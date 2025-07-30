#!/usr/bin/env python3
"""
REST Whatever CLI
使用 Fire 库提供命令行接口
"""
import os
import sys
from pathlib import Path
from typing import Optional

import fire
import uvicorn


def serve(
    host: str = "0.0.0.0",
    port: int = 8000,
    reload: bool = True,
    workers: int = 1,
    log_level: str = "info",
    access_log: bool = True,
    config: Optional[str] = None,
):
    """启动 REST API 服务器

    Args:
        host: 服务器主机地址
        port: 服务器端口
        reload: 是否启用热重载
        workers: 工作进程数量（reload=True 时忽略）
        log_level: 日志级别
        access_log: 是否启用访问日志
        config: 配置文件路径（支持 .yaml, .yml, .toml, .json），空从env读取
    """
    # 设置配置文件环境变量，供应用读取
    if config:
        config_path = Path(config)
        if not config_path.exists():
            print(f"错误: 配置文件不存在: {config}")
            sys.exit(1)

        # 设置环境变量告诉应用使用配置文件
        os.environ["REST_WHATEVER_CONFIG"] = str(config_path.absolute())
        print(f"使用配置文件: {config_path.absolute()}")
    else:
        # 清除配置文件环境变量，使用环境变量配置
        os.environ.pop("REST_WHATEVER_CONFIG", None)
        print("使用环境变量配置")

    uvicorn.run(
        "rest_whatever.app:app",
        host=host,
        port=port,
        reload=reload,
        workers=workers if not reload else None,
        log_level=log_level,
        access_log=access_log,
    )


def create_config(output: str = "config.yaml", format: str = "yaml"):
    """创建示例配置文件

    Args:
        output: 输出文件路径
        format: 配置文件格式 (yaml/toml/json)
    """
    output_path = Path(output)

    if output_path.exists():
        response = input(f"文件 {output} 已存在，是否覆盖？ (y/N): ")
        if response.lower() != "y":
            print("操作已取消")
            return

    format = format.lower()

    if format in ["yaml", "yml"]:
        content = """# REST Whatever 数据库配置文件

# 单数据库配置示例
database_url: "sqlite+aiosqlite:///./app.db"
echo_sql: false
auto_create_tables: true

---
# 多数据库配置示例
databases:
  primary:
    database_url: "mysql+aiomysql://user:password@localhost:3306/primary_db"
    echo_sql: false
    auto_create_tables: true
    # API访问认证配置（可选）
    auth_username: "admin"
    auth_password: "secret123"

  secondary:
    database_url: "postgresql+asyncpg://user:password@localhost:5432/secondary_db"
    echo_sql: true
    auto_create_tables: false
    # 无认证配置，该数据库的API不需要认证

  cache:
    database_url: "sqlite+aiosqlite:///./cache.db"
    echo_sql: false
    auto_create_tables: true
    # 需要认证的SQLite数据库
    auth_username: "cache_user"
    auth_password: "cache_pass"

default_database: "primary"
"""
    elif format == "toml":
        content = """# REST Whatever 数据库配置文件

# 单数据库配置示例
database_url = "sqlite+aiosqlite:///./app.db"
echo_sql = false
auto_create_tables = true

# 多数据库配置示例
[databases.primary]
database_url = "mysql+aiomysql://user:password@localhost:3306/primary_db"
echo_sql = false
auto_create_tables = true
# API访问认证配置（可选）
auth_username = "admin"
auth_password = "secret123"

[databases.secondary]
database_url = "postgresql+asyncpg://user:password@localhost:5432/secondary_db"
echo_sql = true
auto_create_tables = false
# 无认证配置，该数据库的API不需要认证

[databases.cache]
database_url = "sqlite+aiosqlite:///./cache.db"
echo_sql = false
auto_create_tables = true
# 需要认证的SQLite数据库
auth_username = "cache_user"
auth_password = "cache_pass"

default_database = "primary"
"""
    elif format == "json":
        content = """{
  "databases": {
    "primary": {
      "database_url": "mysql+aiomysql://user:password@localhost:3306/primary_db",
      "echo_sql": false,
      "auto_create_tables": true,
      "auth_username": "admin",
      "auth_password": "secret123"
    },
    "secondary": {
      "database_url": "postgresql+asyncpg://user:password@localhost:5432/secondary_db",
      "echo_sql": true,
      "auto_create_tables": false
    },
    "cache": {
      "database_url": "sqlite+aiosqlite:///./cache.db",
      "echo_sql": false,
      "auto_create_tables": true,
      "auth_username": "cache_user",
      "auth_password": "cache_pass"
    }
  },
  "default_database": "primary"
}
"""
    else:
        print(f"❌ 不支持的格式: {format}。支持的格式: yaml, toml, json")
        return

    output_path.write_text(content, encoding="utf-8")
    print(f"✅ 示例配置文件已创建: {output_path.absolute()}")


def serve_cli():
    fire.Fire(serve)


def create_config_cli():
    fire.Fire(create_config)


def main():
    fire.Fire({"serve": serve, "create_config": create_config})
