from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request
from sqlalchemy import func, select

from rest_whatever.database import DatabaseManager
from rest_whatever.models import UpsertRequest, UpsertResponse
from rest_whatever.utils import (
    build_query_filters,
    convert_record_to_dict,
    create_index_if_needed,
    parse_query_conditions,
)

router = APIRouter(prefix="/databases/{db_name}/tables/{table_name}", tags=["数据记录"])


def create_records_router(db_manager: DatabaseManager):
    """创建数据记录路由"""

    @router.get("/")
    async def get_records(
        db_name: str,
        table_name: str,
        request: Request,
        limit: int | None = Query(100, description="返回记录数限制"),
        offset: int | None = Query(0, description="偏移量"),
        auto_index: bool | None = Query(False, description="是否自动创建索引"),
    ):
        """获取指定数据库表的记录，支持复杂查询条件"""
        # 获取正确的数据库会话
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as db:
            try:
                base = db_manager.get_base(db_name)
                if table_name not in base.classes:
                    await db_manager.refresh_automap(db_name)
                    base = db_manager.get_base(db_name)
                    if table_name not in base.classes:
                        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                table_class = base.classes[table_name]

                # 解析查询参数
                query_params = dict(request.query_params)
                conditions = parse_query_conditions(query_params)

                # 构建查询
                stmt = select(table_class)

                # 应用过滤条件
                if conditions:
                    filters = build_query_filters(table_class, conditions)
                    stmt = stmt.where(*filters)

                    # 如果启用了自动索引，检查并创建索引
                    if auto_index:
                        used_columns = [cond.column for cond in conditions]
                        await create_index_if_needed(table_name, used_columns, db_name, db_manager, auto_index)

                # 应用分页
                if offset:
                    stmt = stmt.offset(offset)
                if limit:
                    stmt = stmt.limit(limit)

                # 执行查询
                result = await db.execute(stmt)
                records = result.scalars().all()

                # 转换为字典列表
                data = [convert_record_to_dict(record, table_class) for record in records]

                # 获取总数
                count_stmt = select(func.count()).select_from(table_class)
                total_result = await db.execute(count_stmt)
                total = total_result.scalar()

                return {
                    "database": db_name,
                    "table": table_name,
                    "data": data,
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "count": len(data),
                }
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

    @router.post("/")
    async def create_record(db_name: str, table_name: str, record_data: dict[str, Any]):
        """在指定数据库的表中创建新记录"""
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as db:
            try:
                base = db_manager.get_base(db_name)
                if table_name not in base.classes:
                    await db_manager.refresh_automap(db_name)
                    base = db_manager.get_base(db_name)
                    if table_name not in base.classes:
                        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                table_class = base.classes[table_name]

                # 创建新记录
                new_record = table_class(**record_data)
                db.add(new_record)
                await db.commit()
                await db.refresh(new_record)

                # 转换为字典
                result = convert_record_to_dict(new_record, table_class)

                return {
                    "message": "记录创建成功",
                    "database": db_name,
                    "table": table_name,
                    "data": result,
                }
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"创建记录失败: {str(e)}")

    @router.put("/{record_id}")
    async def update_record(
        db_name: str,
        table_name: str,
        record_id: int,
        record_data: dict[str, Any],
    ):
        """更新指定数据库表中的记录"""
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as db:
            try:
                base = db_manager.get_base(db_name)
                if table_name not in base.classes:
                    await db_manager.refresh_automap(db_name)
                    base = db_manager.get_base(db_name)
                    if table_name not in base.classes:
                        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                table_class = base.classes[table_name]

                # 查找记录
                stmt = select(table_class).where(table_class.id == record_id)
                result = await db.execute(stmt)
                record = result.scalar_one_or_none()

                if not record:
                    raise HTTPException(status_code=404, detail=f"记录 ID {record_id} 不存在")

                # 更新字段
                for key, value in record_data.items():
                    if hasattr(record, key):
                        setattr(record, key, value)

                await db.commit()
                await db.refresh(record)

                # 转换为字典
                result_data = convert_record_to_dict(record, table_class)

                return {
                    "message": "记录更新成功",
                    "database": db_name,
                    "table": table_name,
                    "data": result_data,
                }
            except HTTPException:
                raise
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"更新记录失败: {str(e)}")

    @router.delete("/{record_id}")
    async def delete_record(db_name: str, table_name: str, record_id: int):
        """删除指定数据库表中的记录"""
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as db:
            try:
                base = db_manager.get_base(db_name)
                if table_name not in base.classes:
                    await db_manager.refresh_automap(db_name)
                    base = db_manager.get_base(db_name)
                    if table_name not in base.classes:
                        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                table_class = base.classes[table_name]

                # 查找并删除记录
                stmt = select(table_class).where(table_class.id == record_id)
                result = await db.execute(stmt)
                record = result.scalar_one_or_none()

                if not record:
                    raise HTTPException(status_code=404, detail=f"记录 ID {record_id} 不存在")

                await db.delete(record)
                await db.commit()

                return {
                    "message": f"记录 ID {record_id} 删除成功",
                    "database": db_name,
                    "table": table_name,
                }
            except HTTPException:
                raise
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"删除记录失败: {str(e)}")

    @router.patch("/", response_model=UpsertResponse)
    async def upsert_record(db_name: str, table_name: str, request: UpsertRequest) -> UpsertResponse:
        """插入或更新记录（UPSERT操作）

        使用PATCH方法实现"有则更新，无则插入"的语义。
        当指定的唯一键/主键发生冲突时，会更新现有记录；否则插入新记录。

        参数说明：
        - data: 要插入或更新的数据
        - conflict_columns: 冲突检测列（不指定则使用主键）
        - update_columns: 冲突时要更新的列（不指定则更新除冲突列外的所有列）
        - insert_only_columns: 仅在插入时设置的列（如created_at）
        """
        session_maker = db_manager.get_session_maker(db_name)

        async with session_maker() as db:
            try:
                base = db_manager.get_base(db_name)
                if table_name not in base.classes:
                    await db_manager.refresh_automap(db_name)
                    base = db_manager.get_base(db_name)
                    if table_name not in base.classes:
                        raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                table_class = base.classes[table_name]
                table_obj = table_class.__table__

                # 获取主键列
                primary_key_columns = [col.name for col in table_obj.primary_key.columns]

                # 确定冲突检测列
                conflict_columns = request.conflict_columns or primary_key_columns
                if not conflict_columns:
                    raise HTTPException(status_code=400, detail="无法确定冲突检测列，表可能没有主键")

                # 验证冲突列是否存在
                table_column_names = [col.name for col in table_obj.columns]
                invalid_columns = [col for col in conflict_columns if col not in table_column_names]
                if invalid_columns:
                    raise HTTPException(
                        status_code=400,
                        detail=f"指定的冲突检测列不存在: {invalid_columns}",
                    )

                # 验证数据中是否包含所有冲突检测列
                missing_conflict_data = [col for col in conflict_columns if col not in request.data]
                if missing_conflict_data:
                    raise HTTPException(
                        status_code=400,
                        detail=f"数据中缺少冲突检测列: {missing_conflict_data}",
                    )

                # 构建查询条件查找现有记录
                filters = []
                for col_name in conflict_columns:
                    col = getattr(table_class, col_name)
                    filters.append(col == request.data[col_name])

                # 查找现有记录
                stmt = select(table_class).where(*filters)
                result = await db.execute(stmt)
                existing_record = result.scalar_one_or_none()

                if existing_record:
                    # 更新现有记录
                    action = "update"

                    # 确定要更新的列
                    if request.update_columns:
                        # 使用指定的更新列
                        update_columns = request.update_columns
                        # 验证更新列是否存在
                        invalid_update_columns = [col for col in update_columns if col not in table_column_names]
                        if invalid_update_columns:
                            raise HTTPException(
                                status_code=400,
                                detail=f"指定的更新列不存在: {invalid_update_columns}",
                            )
                    else:
                        # 更新除冲突检测列外的所有列
                        update_columns = [
                            col
                            for col in request.data.keys()
                            if col not in conflict_columns and col in table_column_names
                        ]

                    # 更新字段
                    updated_count = 0
                    for col_name in update_columns:
                        if col_name in request.data and hasattr(existing_record, col_name):
                            old_value = getattr(existing_record, col_name)
                            new_value = request.data[col_name]
                            if old_value != new_value:
                                setattr(existing_record, col_name, new_value)
                                updated_count += 1

                    await db.commit()
                    await db.refresh(existing_record)

                    result_data = convert_record_to_dict(existing_record, table_class)
                    message = f"记录已更新，共更新 {updated_count} 个字段"
                    affected_rows = 1 if updated_count > 0 else 0

                else:
                    # 插入新记录
                    action = "insert"

                    # 准备插入数据
                    insert_data = request.data.copy()

                    # 添加仅插入时的列
                    if request.insert_only_columns:
                        for col_name in request.insert_only_columns:
                            if col_name in request.data and col_name not in insert_data:
                                insert_data[col_name] = request.data[col_name]

                    # 创建新记录
                    new_record = table_class(**insert_data)
                    db.add(new_record)
                    await db.commit()
                    await db.refresh(new_record)

                    result_data = convert_record_to_dict(new_record, table_class)
                    message = "新记录已插入"
                    affected_rows = 1

                return UpsertResponse(
                    success=True,
                    action=action,
                    message=message,
                    database=db_name,
                    table=table_name,
                    data=result_data,
                    affected_rows=affected_rows,
                )

            except HTTPException:
                raise
            except Exception as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"UPSERT操作失败: {str(e)}")

    return router
