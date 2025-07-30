"""
认证中间件
根据路径中的数据库名称动态应用认证
"""

import re
from typing import Callable

from fastapi import Request, Response, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.base import BaseHTTPMiddleware

from rest_whatever.auth import verify_credentials
from rest_whatever.config import MultiDatabaseConfig

security = HTTPBasic()


class DatabaseAuthMiddleware(BaseHTTPMiddleware):
    """数据库认证中间件"""

    def __init__(self, app, multi_config: MultiDatabaseConfig):
        super().__init__(app)
        self.multi_config = multi_config
        # 匹配包含数据库名称的路径模式
        self.db_path_pattern = re.compile(r"^/databases/([^/]+)")

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 检查是否是需要认证的数据库路径
        path = request.url.path
        match = self.db_path_pattern.match(path)

        if match:
            db_name = match.group(1)

            # 跳过数据库管理本身的路由（添加、删除数据库等）
            if path == f"/databases/{db_name}" or path == "/databases" or path == "/databases/":
                return await call_next(request)

            # 获取数据库配置
            db_config = self.multi_config.get_database(db_name)
            if not db_config:
                return Response(content=f"数据库 '{db_name}' 不存在", status_code=status.HTTP_404_NOT_FOUND)

            # 如果数据库需要认证，验证凭据
            if db_config.requires_auth():
                auth_header = request.headers.get("authorization")
                if not auth_header or not auth_header.startswith("Basic "):
                    return Response(
                        content="需要Basic认证",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        headers={"WWW-Authenticate": "Basic"},
                    )

                try:
                    import base64

                    # 解析Basic Auth凭据
                    encoded_credentials = auth_header.split(" ")[1]
                    decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
                    username, password = decoded_credentials.split(":", 1)

                    credentials = HTTPBasicCredentials(username=username, password=password)

                    if not verify_credentials(credentials, db_config):
                        return Response(
                            content="认证失败：用户名或密码错误",
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            headers={"WWW-Authenticate": "Basic"},
                        )
                except Exception:
                    return Response(
                        content="认证凭据格式错误",
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        headers={"WWW-Authenticate": "Basic"},
                    )

        return await call_next(request)
