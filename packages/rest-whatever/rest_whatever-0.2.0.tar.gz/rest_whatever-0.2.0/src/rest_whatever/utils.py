import io
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import polars as pl
from fastapi import HTTPException, UploadFile
from sqlalchemy import Index, MetaData, Table, text

from rest_whatever.models import FileUploadRequest, QueryCondition, UploadResult

logger = logging.getLogger(__name__)


def parse_query_conditions(query_params: dict[str, str]) -> list[QueryCondition]:
    """解析URL查询参数为查询条件"""
    conditions = []

    # 排除特殊参数
    special_params = {"limit", "offset", "auto_index"}

    for param, value in query_params.items():
        if param in special_params:
            continue

        # 解析操作符
        if "__" in param:
            column, operator = param.rsplit("__", 1)
        else:
            column, operator = param, "eq"

        # 处理特殊值类型
        if operator == "in":
            parsed_value = [v.strip() for v in value.split(",")]
        elif operator == "between":
            values = [v.strip() for v in value.split(",")]
            if len(values) != 2:
                raise HTTPException(status_code=400, detail="between操作符需要两个值，用逗号分隔")
            parsed_value = values
        else:
            parsed_value = value

        conditions.append(QueryCondition(column=column, operator=operator, value=parsed_value))

    return conditions


def build_query_filters(table_class, conditions: list[QueryCondition]):
    """根据查询条件构建SQLAlchemy过滤器"""
    filters = []

    for condition in conditions:
        if not hasattr(table_class, condition.column):
            raise HTTPException(status_code=400, detail=f"列 '{condition.column}' 不存在")

        column_attr = getattr(table_class, condition.column)

        if condition.operator == "eq":
            filters.append(column_attr == condition.value)
        elif condition.operator == "ne":
            filters.append(column_attr != condition.value)
        elif condition.operator == "gt":
            filters.append(column_attr > condition.value)
        elif condition.operator == "gte":
            filters.append(column_attr >= condition.value)
        elif condition.operator == "lt":
            filters.append(column_attr < condition.value)
        elif condition.operator == "lte":
            filters.append(column_attr <= condition.value)
        elif condition.operator == "like":
            filters.append(column_attr.like(f"%{condition.value}%"))
        elif condition.operator == "in":
            filters.append(column_attr.in_(condition.value))
        elif condition.operator == "between":
            if isinstance(condition.value, list) and len(condition.value) == 2:
                filters.append(column_attr.between(condition.value[0], condition.value[1]))
            else:
                raise HTTPException(status_code=400, detail="between操作符需要两个值的列表")
        else:
            raise HTTPException(status_code=400, detail=f"不支持的操作符: {condition.operator}")

    return filters


async def create_index_if_needed(table_name: str, columns: list[str], db_name: str, db_manager, auto_index: bool):
    """如果需要且启用了自动索引，创建索引"""
    if not auto_index or not columns:
        return

    try:
        inspector = await db_manager.get_inspector(db_name)
        existing_indexes = inspector.get_indexes(table_name)

        # 检查是否已存在包含这些列的索引
        for index in existing_indexes:
            if set(columns).issubset(set(index["column_names"])):
                logger.info(f"表 {table_name} 已存在包含列 {columns} 的索引: {index['name']}")
                return

        # 创建新索引
        index_name = f"auto_idx_{table_name}_{'_'.join(columns)}"
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as session:
            metadata = MetaData()
            await session.run_sync(lambda sync_session: metadata.reflect(bind=sync_session.bind))
            table = metadata.tables.get(table_name)

            if table is not None:
                index_columns = [table.c[col] for col in columns if col in table.c]
                if index_columns:
                    index = Index(index_name, *index_columns)
                    await session.run_sync(lambda sync_session: index.create(bind=sync_session.bind))
                    await session.commit()
                    logger.info(f"为表 {table_name} 创建索引 {index_name} (列: {columns})")

    except Exception as e:
        logger.warning(f"创建索引失败: {e}")


def convert_record_to_dict(record, table_class) -> dict:
    """将数据库记录转换为字典"""
    result = {}
    for column in table_class.__table__.columns:
        value = getattr(record, column.name, None)
        if isinstance(value, datetime):
            value = value.isoformat()
        result[column.name] = value
    return result


async def process_upload_file(
    file: UploadFile,
    config: FileUploadRequest,
    db_name: str,
    db_manager,
) -> UploadResult:
    """处理上传的文件"""
    start_time = time.time()
    errors = []
    records_processed = 0
    records_inserted = 0
    records_failed = 0

    try:
        # 读取文件内容
        content = await file.read()

        # 确定文件类型
        file_extension = Path(file.filename or "").suffix.lower()

        # 解析文件数据
        if file_extension == ".jsonl" or file_extension == ".ndjson":
            data = parse_jsonlines(content, config.encoding)
        elif file_extension == ".csv":
            data = parse_csv(content, config)
        elif file_extension == ".parquet":
            data = parse_parquet(content)
        elif file_extension == ".sql":
            # SQL文件特殊处理
            return await execute_sql_file(content, config, db_name, db_manager, start_time)
        else:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式: {file_extension}，支持的格式: .jsonl, .csv, .parquet, .sql",
            )

        if data.is_empty():
            return UploadResult(
                success=False,
                message="文件为空或无法解析数据",
                database=db_name,
                table=config.table_name,
                records_processed=0,
                records_inserted=0,
                records_failed=0,
                execution_time=time.time() - start_time,
                errors=["文件为空"],
            )

        records_processed = len(data)

        # 插入数据到数据库
        records_inserted, records_failed, insert_errors = await insert_dataframe_to_db(
            data, config, db_name, db_manager
        )
        errors.extend(insert_errors)

        execution_time = time.time() - start_time

        return UploadResult(
            success=records_failed == 0,
            message=f"成功处理 {records_inserted} 条记录"
            + (f"，失败 {records_failed} 条" if records_failed > 0 else ""),
            database=db_name,
            table=config.table_name,
            records_processed=records_processed,
            records_inserted=records_inserted,
            records_failed=records_failed,
            execution_time=execution_time,
            errors=errors,
        )

    except Exception as e:
        execution_time = time.time() - start_time
        return UploadResult(
            success=False,
            message=f"处理文件失败: {str(e)}",
            database=db_name,
            table=config.table_name,
            records_processed=records_processed,
            records_inserted=records_inserted,
            records_failed=records_processed,
            execution_time=execution_time,
            errors=[str(e)],
        )


def parse_jsonlines(content: bytes, encoding: str = "utf-8") -> pl.DataFrame:
    """解析JSON Lines格式文件"""
    try:
        text_content = content.decode(encoding)
        lines = text_content.strip().split("\n")
        data = []

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                data.append(record)
            except json.JSONDecodeError as e:
                raise ValueError(f"第 {line_num} 行JSON格式错误: {e}")

        if not data:
            return pl.DataFrame()

        return pl.DataFrame(data)
    except UnicodeDecodeError:
        raise ValueError(f"文件编码错误，请确认文件编码为 {encoding}")


def parse_csv(content: bytes, config: FileUploadRequest) -> pl.DataFrame:
    """解析CSV格式文件"""
    try:
        # 使用polars读取CSV
        df = pl.read_csv(
            io.BytesIO(content),
            encoding=config.encoding,
            separator=config.csv_delimiter,
            quote_char=config.csv_quote_char,
            has_header=True,  # 假设第一行是header
        )
        return df
    except Exception as e:
        raise ValueError(f"CSV文件解析错误: {e}")


def parse_parquet(content: bytes) -> pl.DataFrame:
    """解析Parquet格式文件"""
    try:
        df = pl.read_parquet(io.BytesIO(content))
        return df
    except Exception as e:
        raise ValueError(f"Parquet文件解析错误: {e}")


async def execute_sql_file(
    content: bytes,
    config: FileUploadRequest,
    db_name: str,
    db_manager,
    start_time: float,
) -> UploadResult:
    """执行SQL文件"""
    try:
        sql_content = content.decode(config.encoding)

        # 分割SQL语句（简单实现，按分号分割）
        statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]

        session_maker = db_manager.get_session_maker(db_name)

        executed_count = 0
        failed_count = 0
        errors = []

        async with session_maker() as db:
            try:
                if config.sql_batch_execute:
                    # 批量执行
                    try:
                        for stmt in statements:
                            if stmt:
                                await db.execute(text(stmt))
                                executed_count += 1
                        await db.commit()
                    except Exception as e:
                        await db.rollback()
                        failed_count = len(statements)
                        errors.append(f"批量执行失败: {e}")
                else:
                    # 逐条执行
                    for i, stmt in enumerate(statements, 1):
                        if stmt:
                            try:
                                await db.execute(text(stmt))
                                await db.commit()
                                executed_count += 1
                            except Exception as e:
                                await db.rollback()
                                failed_count += 1
                                errors.append(f"第 {i} 条SQL执行失败: {e}")

                # 刷新自动映射
                if executed_count > 0:
                    await db_manager.refresh_automap(db_name)

            except Exception as e:
                await db.rollback()
                raise e

        execution_time = time.time() - start_time

        return UploadResult(
            success=failed_count == 0,
            message=f"执行了 {executed_count} 条SQL语句" + (f"，失败 {failed_count} 条" if failed_count > 0 else ""),
            database=db_name,
            table=config.table_name,
            records_processed=len(statements),
            records_inserted=executed_count,
            records_failed=failed_count,
            execution_time=execution_time,
            errors=errors,
        )

    except UnicodeDecodeError:
        execution_time = time.time() - start_time
        return UploadResult(
            success=False,
            message=f"SQL文件编码错误，请确认文件编码为 {config.encoding}",
            database=db_name,
            table=config.table_name,
            records_processed=0,
            records_inserted=0,
            records_failed=1,
            execution_time=execution_time,
            errors=["文件编码错误"],
        )


async def insert_dataframe_to_db(
    df: pl.DataFrame, config: FileUploadRequest, db_name: str, db_manager
) -> tuple[int, int, list[str]]:
    """将DataFrame数据插入到数据库"""
    session_maker = db_manager.get_session_maker(db_name)
    errors = []
    records_inserted = 0
    records_failed = 0

    async with session_maker() as db:
        try:
            # 检查表是否存在
            base = db_manager.get_base(db_name)
            table_exists = config.table_name in base.classes

            if not table_exists and not config.create_table:
                raise ValueError(f"表 '{config.table_name}' 不存在，且未启用自动创建表")

            if not table_exists and config.create_table:
                # 自动创建表
                await create_table_from_dataframe(df, config.table_name, db_name, db_manager)
                # 刷新自动映射
                await db_manager.refresh_automap(db_name)
                base = db_manager.get_base(db_name)

            if config.table_name not in base.classes:
                raise ValueError(f"无法访问表 '{config.table_name}'")

            table_class = base.classes[config.table_name]

            # 处理不同的插入策略
            if config.if_exists == "replace":
                # 清空表
                from sqlalchemy import delete

                stmt = delete(table_class)
                await db.execute(stmt)
                await db.commit()
            elif config.if_exists == "fail":
                # 检查表是否有数据
                from sqlalchemy import func, select

                count_stmt = select(func.count()).select_from(table_class)
                result = await db.execute(count_stmt)
                count = result.scalar()
                if count > 0:
                    raise ValueError(f"表 '{config.table_name}' 已有数据，且配置为fail模式")

            # 批量插入数据
            batch_size = config.batch_size
            total_records = len(df)

            # 将polars DataFrame转换为字典列表进行批处理
            df_dicts = df.to_dicts()

            for start_idx in range(0, total_records, batch_size):
                end_idx = min(start_idx + batch_size, total_records)
                batch_data = df_dicts[start_idx:end_idx]

                batch_records = []
                for i, record_data in enumerate(batch_data):
                    try:
                        # 处理None值和类型转换
                        cleaned_data = {}
                        for k, v in record_data.items():
                            if v is None:
                                cleaned_data[k] = None
                            elif isinstance(v, float) and str(v) == "nan":
                                cleaned_data[k] = None
                            else:
                                cleaned_data[k] = v

                        # 创建记录对象
                        record = table_class(**cleaned_data)
                        batch_records.append(record)
                    except Exception as e:
                        records_failed += 1
                        errors.append(f"记录 {start_idx + i} 处理失败: {e}")

                # 批量插入
                if batch_records:
                    try:
                        db.add_all(batch_records)
                        await db.commit()
                        records_inserted += len(batch_records)
                    except Exception as e:
                        await db.rollback()
                        records_failed += len(batch_records)
                        errors.append(f"批量插入失败 (记录 {start_idx}-{end_idx}): {e}")

        except Exception as e:
            await db.rollback()
            raise e

    return records_inserted, records_failed, errors


async def create_table_from_dataframe(df: pl.DataFrame, table_name: str, db_name: str, db_manager) -> None:
    """根据DataFrame的结构自动创建表"""
    from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text

    session_maker = db_manager.get_session_maker(db_name)
    metadata = MetaData()

    # 使用列表存储所有列定义，避免类型检查器错误
    table_columns: list[Column[Any]] = [Column("id", Integer(), primary_key=True, autoincrement=True)]

    # 推断列类型 - Polars版本
    for col_name in df.columns:
        col_dtype = df[col_name].dtype

        if col_dtype == pl.Int64 or col_dtype == pl.Int32:
            table_columns.append(Column(col_name, Integer(), nullable=True))
        elif col_dtype == pl.Float64 or col_dtype == pl.Float32:
            table_columns.append(Column(col_name, Float(), nullable=True))
        elif col_dtype == pl.Boolean:
            table_columns.append(Column(col_name, Boolean(), nullable=True))
        elif col_dtype == pl.Datetime or col_dtype == pl.Date:
            table_columns.append(Column(col_name, DateTime(), nullable=True))
        elif col_dtype == pl.Utf8:
            # 字符串类型，检查最大长度
            col_series = df[col_name].drop_nulls()
            if len(col_series) > 0:
                max_length = col_series.str.len_chars().max()
                # 类型检查：确保max_length是数字
                if max_length and isinstance(max_length, (int, float)) and max_length > 255:
                    table_columns.append(Column(col_name, Text(), nullable=True))
                else:
                    # 安全的长度计算
                    safe_length = 255
                    if max_length and isinstance(max_length, (int, float)):
                        safe_length = max(255, int(max_length * 1.2))
                    table_columns.append(
                        Column(
                            col_name,
                            String(safe_length),
                            nullable=True,
                        )
                    )
            else:
                table_columns.append(Column(col_name, Text(), nullable=True))
        else:
            # 其他类型默认为文本
            table_columns.append(Column(col_name, Text(), nullable=True))

    # 创建表
    Table(table_name, metadata, *table_columns)

    async with session_maker() as session:
        await session.run_sync(lambda sync_session: metadata.create_all(bind=sync_session.bind))
        await session.commit()
