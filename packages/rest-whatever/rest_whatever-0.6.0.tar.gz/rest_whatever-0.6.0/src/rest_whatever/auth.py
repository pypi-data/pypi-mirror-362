"""
身份认证模块
提供Basic Auth认证功能
"""

import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from rest_whatever.config import DatabaseConfig

security = HTTPBasic()


def verify_credentials(credentials: HTTPBasicCredentials, config: DatabaseConfig) -> bool:
    """验证用户凭据"""
    if not config.requires_auth():
        return True

    correct_username = (
        secrets.compare_digest(credentials.username.encode("utf8"), config.auth_username.encode("utf8"))
        if config.auth_username
        else False
    )

    correct_password = (
        secrets.compare_digest(credentials.password.encode("utf8"), config.auth_password.encode("utf8"))
        if config.auth_password
        else False
    )

    return correct_username and correct_password


def create_auth_dependency(db_config: DatabaseConfig):
    """创建特定数据库的认证依赖"""

    def auth_required(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
        if not db_config.requires_auth():
            return True

        if not verify_credentials(credentials, db_config):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证失败：用户名或密码错误",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True

    return auth_required


def create_conditional_auth_dependency(get_db_config_func):
    """创建条件认证依赖，根据数据库配置决定是否需要认证"""

    def conditional_auth(db_name: str, credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
        db_config = get_db_config_func(db_name)
        if not db_config:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"数据库 '{db_name}' 不存在")

        if not db_config.requires_auth():
            return True

        if not verify_credentials(credentials, db_config):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="认证失败：用户名或密码错误",
                headers={"WWW-Authenticate": "Basic"},
            )
        return True

    return conditional_auth
