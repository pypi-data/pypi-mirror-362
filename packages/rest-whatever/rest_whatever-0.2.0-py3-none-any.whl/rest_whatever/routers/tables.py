from typing import Any

from fastapi import APIRouter, HTTPException
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    Text,
)

from rest_whatever.database import DatabaseManager
from rest_whatever.models import (
    ColumnInfo,
    IndexCreateRequest,
    IndexInfo,
    TableCreateRequest,
    TableSchemaResponse,
)

router = APIRouter(prefix="/databases/{db_name}/tables", tags=["表管理"])


def create_tables_router(db_manager: DatabaseManager):
    """创建表管理路由"""

    @router.get("/")
    async def list_tables(db_name: str):
        """获取指定数据库的表列表"""
        try:
            table_names = await db_manager.get_table_names(db_name)
            return {"database": db_name, "tables": table_names}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取表列表失败: {str(e)}")

    @router.post("/")
    async def create_table(db_name: str, request: TableCreateRequest):
        """在指定数据库中创建新表"""
        try:
            session_maker = db_manager.get_session_maker(db_name)
            metadata = MetaData()

            # 构建列定义
            columns: list[Column[Any]] = []
            for col_name, col_def in request.columns.items():
                col_type = col_def.get("type", "String")
                nullable = col_def.get("nullable", True)
                primary_key = col_def.get("primary_key", False)

                # 映射类型
                if col_type.lower() == "integer":
                    column_type = Integer()
                elif col_type.lower() == "string":
                    column_type = String(col_def.get("length", 255))
                elif col_type.lower() == "text":
                    column_type = Text()
                elif col_type.lower() == "boolean":
                    column_type = Boolean()
                elif col_type.lower() == "float":
                    column_type = Float()
                elif col_type.lower() == "datetime":
                    column_type = DateTime()
                else:
                    column_type = Text()

                columns.append(
                    Column(
                        col_name,
                        column_type,
                        nullable=nullable,
                        primary_key=primary_key,
                        index=col_def.get("index", False),
                        unique=col_def.get("unique", False),
                    )
                )

            # 如果没有主键，添加一个默认的id主键
            if not any(col.primary_key for col in columns):
                columns.insert(0, Column("id", Integer(), primary_key=True, autoincrement=True))

            # 创建表
            Table(request.table_name, metadata, *columns)

            async with session_maker() as session:
                await session.run_sync(lambda sync_session: metadata.create_all(bind=sync_session.bind))
                await session.commit()

            # 刷新自动映射
            await db_manager.refresh_automap(db_name)

            return {"message": f"表 '{request.table_name}' 创建成功"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建表失败: {str(e)}")

    @router.delete("/{table_name}")
    async def drop_table(db_name: str, table_name: str):
        """删除指定数据库中的表"""
        try:
            session_maker = db_manager.get_session_maker(db_name)
            metadata = MetaData()

            async with session_maker() as session:
                # 反射表结构
                await session.run_sync(lambda sync_session: metadata.reflect(bind=sync_session.bind))
                table = metadata.tables.get(table_name)
                if table is None:
                    raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                # 删除表
                await session.run_sync(lambda sync_session: table.drop(bind=sync_session.bind))
                await session.commit()

            # 刷新自动映射
            await db_manager.refresh_automap(db_name)

            return {"message": f"表 '{table_name}' 删除成功"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"删除表失败: {str(e)}")

    @router.get("/{table_name}/schema", response_model=TableSchemaResponse)
    async def get_table_schema(db_name: str, table_name: str) -> TableSchemaResponse:
        """获取指定数据库中表的结构"""
        try:
            await db_manager.refresh_automap(db_name)
            columns = db_manager.get_table_columns(db_name, table_name)
            indexes = db_manager.get_table_indexes(db_name, table_name)
            primary_keys = db_manager.get_table_primary_key(db_name, table_name)

            return TableSchemaResponse(
                database=db_name,
                table_name=table_name,
                columns=[
                    ColumnInfo(
                        name=column.name,
                        is_primary_key=column.primary_key,
                        is_nullable=column.nullable,
                        type=str(column.type),
                        detail=str(column),
                    )
                    for column in columns
                ],
                indexes=[
                    IndexInfo(
                        name=index.name,
                        cols=[col.name for col in index.columns if col.name is not None],
                    )
                    for index in indexes
                ],
                primary_keys=[pk.name for pk in primary_keys],
            )
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail=f"表 '{table_name}' 不存在或获取结构失败: {str(e)}",
            )

    @router.post("/{table_name}/indexes")
    async def create_index(db_name: str, table_name: str, request: IndexCreateRequest):
        """在指定数据库的表中创建索引"""
        try:
            session_maker = db_manager.get_session_maker(db_name)

            async with session_maker() as session:
                # 反射表结构获取表对象
                metadata = MetaData()
                await session.run_sync(lambda sync_session: metadata.reflect(bind=sync_session.bind))
                table = metadata.tables.get(table_name)

                if table is None:
                    raise HTTPException(status_code=404, detail=f"表 '{table_name}' 不存在")

                index_columns = [table.c[col] for col in request.columns if col in table.c]

                if not index_columns:
                    raise HTTPException(status_code=400, detail="指定的列不存在")

                index = Index(request.index_name, *index_columns, unique=request.unique)
                await session.run_sync(lambda sync_session: index.create(bind=sync_session.bind))
                await session.commit()

            await db_manager.refresh_automap(db_name)
            return {"message": f"索引 '{request.index_name}' 创建成功"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"创建索引失败: {str(e)}")

    return router
