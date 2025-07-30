#!/usr/bin/env python3
"""
REST Whatever CLI
使用 Fire 库提供命令行接口
"""
import logging
import sys
from typing import Optional

import fire
import uvicorn

from rest_whatever.config import MultiDatabaseConfig


class RestWhateverCLI:
    """REST Whatever 命令行工具"""

    def __init__(self):
        """初始化 CLI"""
        self.logger = self._setup_logging()

    def _setup_logging(self, level: str = "INFO") -> logging.Logger:
        """设置日志"""
        log_level = getattr(logging, level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        return logging.getLogger(__name__)

    def serve(
        self,
        host: str = "0.0.0.0",
        port: int = 8000,
        reload: bool = True,
        workers: int = 1,
        log_level: str = "info",
        access_log: bool = True,
    ):
        """
        启动 REST API 服务

        Args:
            host: 服务监听地址 (默认: 0.0.0.0)
            port: 服务端口 (默认: 8000)
            reload: 是否启用热重载 (默认: True)
            workers: 工作进程数 (默认: 1)
            log_level: 日志级别 (默认: info)
            access_log: 是否启用访问日志 (默认: True)
        """
        self.logger.info(f"启动 REST Whatever 服务...")
        self.logger.info(f"服务地址: http://{host}:{port}")

        # 生产环境配置
        if not reload and workers > 1:
            self.logger.info(f"生产模式: 使用 {workers} 个工作进程")
        elif reload:
            self.logger.info("开发模式: 启用热重载")

        try:
            uvicorn.run(
                "rest_whatever.main:app",
                host=host,
                port=port,
                reload=reload,
                workers=workers if not reload else None,
                log_level=log_level,
                access_log=access_log,
            )
        except KeyboardInterrupt:
            self.logger.info("服务已停止")
        except Exception as e:
            self.logger.error(f"启动服务时出错: {e}")
            sys.exit(1)

    def dev(self, host: str = "127.0.0.1", port: int = 8000):
        """
        启动开发服务器 (热重载模式)

        Args:
            host: 服务监听地址 (默认: 127.0.0.1)
            port: 服务端口 (默认: 8000)
        """
        self.logger.info("启动开发服务器...")
        self.serve(host=host, port=port, reload=True, workers=1, log_level="debug")

    def prod(self, host: str = "0.0.0.0", port: int = 8000, workers: int = 4):
        """
        启动生产服务器 (多进程模式)

        Args:
            host: 服务监听地址 (默认: 0.0.0.0)
            port: 服务端口 (默认: 8000)
            workers: 工作进程数 (默认: 4)
        """
        self.logger.info("启动生产服务器...")
        self.serve(
            host=host,
            port=port,
            reload=False,
            workers=workers,
            log_level="info",
            access_log=True,
        )

    def _parse_database_url(self, database_url: str) -> dict:
        """解析数据库连接 URL"""
        import re

        # 匹配不同数据库的 URL 格式
        patterns = {
            "sqlite": r"sqlite(\+aiosqlite)?://(/.*)",
            "mysql": r"mysql(\+aiomysql)?://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)",
            "postgresql": r"postgresql(\+asyncpg)?://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)",
        }

        for db_type, pattern in patterns.items():
            match = re.match(pattern, database_url)
            if match:
                if db_type == "sqlite":
                    return {
                        "type": "SQLite",
                        "path": match.group(2),
                        "host": "N/A",
                        "port": "N/A",
                        "database": "N/A",
                        "username": "N/A",
                    }
                else:
                    return {
                        "type": db_type.upper(),
                        "username": match.group(2),
                        "password": "***" if match.group(3) else "N/A",
                        "host": match.group(4),
                        "port": match.group(5),
                        "database": match.group(6),
                        "path": "N/A",
                    }

        return {
            "type": "Unknown",
            "url": database_url,
            "host": "N/A",
            "port": "N/A",
            "database": "N/A",
            "username": "N/A",
        }

    def config(self, action: str = "show", db_name: Optional[str] = None):
        """
        管理数据库配置

        Args:
            action: 操作类型 (show/list/test)
            db_name: 数据库名称 (可选)
        """
        try:
            multi_config = MultiDatabaseConfig.from_env()
        except Exception as e:
            self.logger.error(f"加载配置失败: {e}")
            return

        if action == "show":
            if db_name:
                config = multi_config.get_database(db_name)
                if config:
                    parsed = self._parse_database_url(config.database_url)
                    self.logger.info(f"数据库 '{db_name}' 配置:")
                    print(f"  名称: {config.name}")
                    print(f"  类型: {parsed['type']}")
                    if parsed["type"] == "SQLite":
                        print(f"  路径: {parsed['path']}")
                    else:
                        print(f"  主机: {parsed['host']}")
                        print(f"  端口: {parsed['port']}")
                        print(f"  数据库: {parsed['database']}")
                        print(f"  用户: {parsed['username']}")
                    print(f"  启用SQL日志: {config.echo_sql}")
                    print(f"  自动创建表: {config.auto_create_tables}")
                else:
                    self.logger.error(f"未找到数据库 '{db_name}' 的配置")
            else:
                self.logger.info("显示所有数据库配置...")
                databases = multi_config.list_databases()
                if databases:
                    for db in databases:
                        config = multi_config.get_database(db)
                        if config:
                            parsed = self._parse_database_url(config.database_url)
                            print(f"\n数据库: {db}")
                            print(f"  类型: {parsed['type']}")
                            if parsed["type"] == "SQLite":
                                print(f"  路径: {parsed['path']}")
                            else:
                                print(f"  主机: {parsed['host']}:{parsed['port']}")
                                print(f"  数据库: {parsed['database']}")
                else:
                    print("未配置任何数据库")

        elif action == "list":
            databases = multi_config.list_databases()
            self.logger.info(f"已配置的数据库 ({len(databases)} 个):")
            for db in databases:
                config = multi_config.get_database(db)
                if config:
                    parsed = self._parse_database_url(config.database_url)
                    print(f"  - {db} ({parsed['type']})")

        elif action == "test":
            self.logger.info("测试数据库连接...")
            # 这里可以添加连接测试逻辑
            print("连接测试功能待实现")

        else:
            self.logger.error(f"未知操作: {action}")
            print("支持的操作: show, list, test")

    def version(self):
        """显示版本信息"""
        print("REST Whatever v1.0.0")
        print("通用多数据库 REST API 服务")

    def health(self, host: str = "127.0.0.1", port: int = 8000):
        """
        检查服务健康状态

        Args:
            host: 服务地址 (默认: 127.0.0.1)
            port: 服务端口 (默认: 8000)
        """
        import httpx

        url = f"http://{host}:{port}/"
        try:
            self.logger.info(f"检查服务健康状态: {url}")
            response = httpx.get(url, timeout=5.0)
            if response.status_code == 200:
                print("✅ 服务运行正常")
                data = response.json()
                print(f"版本: {data.get('version', 'unknown')}")
                print(f"数据库数量: {len(data.get('databases', []))}")
            else:
                print(f"❌ 服务响应异常: {response.status_code}")
        except httpx.ConnectError:
            print("❌ 无法连接到服务")
        except httpx.TimeoutException:
            print("❌ 连接超时")
        except Exception as e:
            print(f"❌ 检查失败: {e}")


def main():
    """CLI 入口点"""
    try:
        fire.Fire(RestWhateverCLI)
    except KeyboardInterrupt:
        print("\n操作已取消")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
