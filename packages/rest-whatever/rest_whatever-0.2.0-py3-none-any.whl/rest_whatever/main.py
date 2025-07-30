import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rest_whatever.config import MultiDatabaseConfig
from rest_whatever.database import DatabaseManager
from rest_whatever.routers.databases import create_database_router
from rest_whatever.routers.records import create_records_router
from rest_whatever.routers.tables import create_tables_router
from rest_whatever.routers.uploads import create_upload_router

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 多数据库配置管理器
multi_config = MultiDatabaseConfig.from_env()

# 初始化数据库管理器
db_manager = DatabaseManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时的初始化
    logger.info("正在初始化数据库连接...")

    # 添加所有配置的数据库
    for db_name in multi_config.list_databases():
        db_config = multi_config.get_database(db_name)
        if db_config:
            try:
                await db_manager.add_database(db_config)
                logger.info(f"数据库 '{db_name}' 初始化成功")
            except Exception as e:
                logger.error(f"数据库 '{db_name}' 初始化失败: {e}")

    logger.info(f"共初始化了 {len(db_manager.list_databases())} 个数据库")

    yield  # 应用运行期间

    # 关闭时的清理
    logger.info("正在清理数据库连接...")
    for db_name in list(db_manager.list_databases()):  # 创建副本避免在迭代时修改
        try:
            await db_manager.remove_database(db_name)
            logger.info(f"数据库 '{db_name}' 连接已关闭")
        except Exception as e:
            logger.error(f"关闭数据库 '{db_name}' 连接时出错: {e}")

    logger.info("所有数据库连接已清理")


# 创建FastAPI应用
app = FastAPI(
    title="通用多数据库REST API",
    description="基于SQLAlchemy Automap的通用多数据库REST API服务，支持文件上传",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """API根路径"""
    return {
        "message": "通用多数据库REST API服务",
        "version": "1.0.0",
        "features": ["多数据库支持", "文件上传", "CRUD操作"],
        "databases": db_manager.list_databases(),
    }


# 注册路由
# 数据库管理路由
database_router = create_database_router(db_manager, multi_config)
app.include_router(database_router)

# 表管理路由
tables_router = create_tables_router(db_manager)
app.include_router(tables_router)

# 数据记录路由
records_router = create_records_router(db_manager)
app.include_router(records_router)

# 文件上传路由
upload_router = create_upload_router(db_manager)
app.include_router(upload_router)


def main():
    import uvicorn

    uvicorn.run("rest_whatever.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
