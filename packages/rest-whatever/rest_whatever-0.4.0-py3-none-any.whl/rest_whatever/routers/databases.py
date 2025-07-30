from fastapi import APIRouter, HTTPException

from rest_whatever.config import MultiDatabaseConfig
from rest_whatever.database import DatabaseManager
from rest_whatever.models import DatabaseAddRequest

router = APIRouter(prefix="/databases", tags=["数据库管理"])


def create_database_router(db_manager: DatabaseManager, multi_config: MultiDatabaseConfig):
    """创建数据库管理路由"""

    @router.get("/")
    async def list_databases():
        """获取所有数据库列表"""
        try:
            databases = db_manager.list_databases()
            return {"databases": databases, "default": multi_config.default_db_name}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取数据库列表失败: {str(e)}")

    @router.post("/")
    async def add_database(request: DatabaseAddRequest):
        """添加新数据库连接"""
        try:
            # 检查数据库名称是否已存在
            if request.name in db_manager.list_databases():
                raise HTTPException(status_code=400, detail=f"数据库 '{request.name}' 已存在")

            # 添加到配置
            multi_config.add_database_from_params(
                name=request.name,
                db_type=request.db_type,
                host=request.host or "localhost",
                port=request.port,
                username=request.username or "",
                password=request.password or "",
                database=request.database or "",
                path=request.path or "",
                echo_sql=request.echo_sql,
                auto_create_tables=request.auto_create_tables,
            )

            # 添加到管理器
            db_config = multi_config.get_database(request.name)
            if db_config:
                await db_manager.add_database(db_config)

            return {"message": f"数据库 '{request.name}' 添加成功"}
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"添加数据库失败: {str(e)}")

    @router.delete("/{db_name}")
    async def remove_database(db_name: str):
        """移除数据库连接"""
        try:
            if db_name not in db_manager.list_databases():
                raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")

            if db_name == multi_config.default_db_name:
                raise HTTPException(status_code=400, detail="不能删除默认数据库")

            # 从管理器中移除
            await db_manager.remove_database(db_name)

            return {"message": f"数据库 '{db_name}' 移除成功"}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"移除数据库失败: {str(e)}")

    return router
