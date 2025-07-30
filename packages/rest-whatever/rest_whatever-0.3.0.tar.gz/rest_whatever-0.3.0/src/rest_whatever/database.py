import logging
from typing import Any

from fastapi import HTTPException
from sqlalchemy import Column, Index, MetaData, PrimaryKeyConstraint
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.sql.base import ReadOnlyColumnCollection

from rest_whatever.config import DatabaseConfig

logger = logging.getLogger(__name__)


class DatabaseManager:
    """异步数据库管理器类"""

    def __init__(self):
        self.engines: dict[str, AsyncEngine] = {}
        self.session_makers: dict[str, async_sessionmaker[AsyncSession]] = {}
        self.bases: dict[str, Any] = {}
        self.metadata_cache: dict[str, MetaData] = {}

    async def add_database(self, config: DatabaseConfig):
        """添加数据库连接"""
        engine = create_async_engine(config.database_url, echo=config.echo_sql)
        session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
        base = automap_base()

        self.engines[config.name] = engine
        self.session_makers[config.name] = session_maker
        self.bases[config.name] = base

        # 尝试初始化自动映射
        try:
            # 异步操作需要在会话中进行
            async with session_maker() as session:
                # 反射数据库表结构
                base.metadata = MetaData()
                await session.run_sync(lambda sync_session: base.metadata.reflect(bind=sync_session.bind))
                base.prepare(autoload_with=None)
                self.metadata_cache[config.name] = base.metadata
        except Exception as e:
            logger.warning(f"数据库 '{config.name}' 初始化自动映射失败: {e}")

    def get_engine(self, db_name: str):
        """获取数据库引擎"""
        if db_name not in self.engines:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        return self.engines[db_name]

    def get_session_maker(self, db_name: str):
        """获取会话制造器"""
        if db_name not in self.session_makers:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        return self.session_makers[db_name]

    def get_base(self, db_name: str):
        """获取自动映射基类"""
        if db_name not in self.bases:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        return self.bases[db_name]

    def get_table_columns(self, db_name: str, table_name: str) -> list[Column]:
        """获取表的列"""
        if db_name not in self.bases:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        base = self.bases[db_name]
        table = base.classes[table_name]
        columns: ReadOnlyColumnCollection = table.__table__.columns
        return list(columns.values())

    def get_table_indexes(self, db_name: str, table_name: str) -> set[Index]:
        """获取表的索引"""
        if db_name not in self.bases:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        base = self.bases[db_name]
        table = base.classes[table_name]
        indexes: set[Index] = table.__table__.indexes
        return indexes

    def get_table_primary_key(self, db_name: str, table_name: str) -> PrimaryKeyConstraint:
        """获取表的主键"""
        if db_name not in self.bases:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")
        base = self.bases[db_name]
        table = base.classes[table_name]
        pks: PrimaryKeyConstraint = table.__table__.primary_key
        return pks

    async def get_table_names(self, db_name: str):
        session_maker = self.get_session_maker(db_name)
        engine = self.engines[db_name]
        async with session_maker() as session:
            async with engine.connect() as conn:
                table_names = await conn.run_sync(session.bind.dialect.get_table_names)
                return table_names

    async def refresh_automap(self, db_name: str):
        """刷新指定数据库的自动映射"""
        if db_name not in self.bases:
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")

        base = self.bases[db_name]
        session_maker = self.session_makers[db_name]

        base.metadata.clear()
        new_base = automap_base()
        new_base.metadata = MetaData()

        async with session_maker() as session:
            await session.run_sync(lambda sync_session: new_base.metadata.reflect(bind=sync_session.bind))
            new_base.prepare(autoload_with=None)

        self.bases[db_name] = new_base
        self.metadata_cache[db_name] = new_base.metadata
        return new_base

    def list_databases(self) -> list[str]:
        """列出所有数据库"""
        return list(self.engines.keys())

    async def remove_database(self, db_name: str):
        """移除数据库连接"""
        # 关闭引擎连接
        if db_name in self.engines:
            await self.engines[db_name].dispose()
            del self.engines[db_name]
        if db_name in self.session_makers:
            del self.session_makers[db_name]
        if db_name in self.bases:
            del self.bases[db_name]
        if db_name in self.metadata_cache:
            del self.metadata_cache[db_name]


async def get_db_session(db_manager: DatabaseManager, db_name: str):
    """获取指定数据库的异步会话"""
    session_maker = db_manager.get_session_maker(db_name)
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
