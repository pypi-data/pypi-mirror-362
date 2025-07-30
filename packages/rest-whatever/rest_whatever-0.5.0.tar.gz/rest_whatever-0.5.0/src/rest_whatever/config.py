import json
import os
import tomllib
from pathlib import Path

import yaml


class DatabaseConfig:
    """单个数据库配置类"""

    def __init__(
        self,
        name: str,
        database_url: str,
        echo_sql: bool = False,
        auto_create_tables: bool = True,
    ):
        self.name = name
        self.database_url = database_url
        self.echo_sql = echo_sql
        self.auto_create_tables = auto_create_tables

    @classmethod
    def from_env(cls, name: str = "default") -> "DatabaseConfig":
        """从环境变量创建配置"""
        database_url = os.getenv("DATABASE_URL", "sqlite:///./test.db")
        echo_sql = os.getenv("ECHO_SQL", "false").lower() == "true"
        auto_create_tables = os.getenv("AUTO_CREATE_TABLES", "true").lower() == "true"

        return cls(
            name=name,
            database_url=database_url,
            echo_sql=echo_sql,
            auto_create_tables=auto_create_tables,
        )

    @classmethod
    def from_config(cls, config_path: str | Path, name: str = "default") -> "DatabaseConfig":
        """从配置文件创建配置，支持 YAML 和 TOML 格式"""
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        suffix = config_path.suffix.lower()

        if suffix in [".yaml", ".yml"]:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

        elif suffix in [".toml"]:
            with open(config_path, "rb") as f:
                config_data = tomllib.load(f)

        elif suffix in [".json"]:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

        else:
            raise ValueError(f"不支持的配置文件格式: {suffix}。支持的格式: .yaml, .yml, .toml, .json")

        # 如果配置文件包含多个数据库配置，选择指定的名称
        if isinstance(config_data, dict) and "databases" in config_data:
            if name not in config_data["databases"]:
                raise ValueError(f"配置文件中未找到数据库配置: {name}")
            db_config = config_data["databases"][name]
        elif isinstance(config_data, dict) and name in config_data:
            db_config = config_data[name]
        else:
            # 假设整个配置文件就是单个数据库的配置
            db_config = config_data

        return cls(
            name=name,
            database_url=db_config["database_url"],
            echo_sql=db_config.get("echo_sql", False),
            auto_create_tables=db_config.get("auto_create_tables", True),
        )

    def get_sqlite_url(self, db_path: str = "./test.db") -> str:
        """获取SQLite连接URL"""
        return f"sqlite+aiosqlite:///{db_path}"

    def get_mysql_url(
        self,
        host: str = "localhost",
        port: int = 3306,
        username: str = "root",
        password: str = "",
        database: str = "test",
    ) -> str:
        """获取MySQL连接URL"""
        return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"

    def get_postgresql_url(
        self,
        host: str = "localhost",
        port: int = 5432,
        username: str = "postgres",
        password: str = "",
        database: str = "test",
    ) -> str:
        """获取PostgreSQL连接URL"""
        return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"


class MultiDatabaseConfig:
    """多数据库配置管理器"""

    def __init__(self):
        self.databases: dict[str, DatabaseConfig] = {}
        self.default_db_name = "default"

    def add_database(self, config: DatabaseConfig):
        """添加数据库配置"""
        self.databases[config.name] = config

    def get_database(self, name: str) -> DatabaseConfig | None:
        """获取数据库配置"""
        return self.databases.get(name)

    def list_databases(self) -> list[str]:
        """列出所有数据库名称"""
        return list(self.databases.keys())

    def set_default_database(self, name: str):
        """设置默认数据库"""
        if name in self.databases:
            self.default_db_name = name
        else:
            raise ValueError(f"数据库 '{name}' 不存在")

    def get_default_database(self) -> DatabaseConfig:
        """获取默认数据库配置"""
        if self.default_db_name in self.databases:
            return self.databases[self.default_db_name]
        raise ValueError("没有设置默认数据库")

    @classmethod
    def from_env(cls) -> "MultiDatabaseConfig":
        """从环境变量创建多数据库配置"""
        config = cls()

        # 尝试从环境变量读取多数据库配置
        multi_db_config = os.getenv("MULTI_DB_CONFIG")
        if multi_db_config:
            try:
                db_configs = json.loads(multi_db_config)
                for db_name, db_config in db_configs.items():
                    database_config = DatabaseConfig(
                        name=db_name,
                        database_url=db_config["database_url"],
                        echo_sql=db_config.get("echo_sql", False),
                        auto_create_tables=db_config.get("auto_create_tables", True),
                    )
                    config.add_database(database_config)

                # 设置默认数据库
                default_db = db_configs.get("_default", list(db_configs.keys())[0] if db_configs else "default")
                if default_db != "_default" and default_db in config.databases:
                    config.set_default_database(default_db)

            except (json.JSONDecodeError, KeyError) as e:
                print(f"解析多数据库配置失败: {e}")

        # 如果没有多数据库配置，使用单数据库配置
        if not config.databases:
            default_config = DatabaseConfig.from_env("default")
            config.add_database(default_config)
            config.set_default_database("default")

        return config

    @classmethod
    def from_config(cls, config_path: str | Path) -> "MultiDatabaseConfig":
        """从配置文件创建多数据库配置，支持 YAML 和 TOML 格式"""
        config_path = Path(config_path)

        if not config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {config_path}")

        suffix = config_path.suffix.lower()

        if suffix in [".yaml", ".yml"]:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)

        elif suffix in [".toml"]:
            with open(config_path, "rb") as f:
                config_data = tomllib.load(f)

        elif suffix in [".json"]:
            with open(config_path, "r", encoding="utf-8") as f:
                config_data = json.load(f)

        else:
            raise ValueError(f"不支持的配置文件格式: {suffix}。支持的格式: .yaml, .yml, .toml, .json")

        config = cls()

        # 处理数据库配置
        databases_config = config_data.get("databases", {})
        if not databases_config and "database_url" in config_data:
            # 如果没有 databases 字段但有 database_url，视为单数据库配置
            databases_config = {"default": config_data}

        for db_name, db_config in databases_config.items():
            database_config = DatabaseConfig(
                name=db_name,
                database_url=db_config["database_url"],
                echo_sql=db_config.get("echo_sql", False),
                auto_create_tables=db_config.get("auto_create_tables", True),
            )
            config.add_database(database_config)

        # 设置默认数据库
        default_db = config_data.get("default_database")
        if default_db and default_db in config.databases:
            config.set_default_database(default_db)
        elif config.databases:
            # 如果没有指定默认数据库，使用第一个
            first_db = list(config.databases.keys())[0]
            config.set_default_database(first_db)

        return config

    def add_database_from_params(
        self,
        name: str,
        db_type: str,
        host: str = "localhost",
        port: int | None = None,
        username: str = "",
        password: str = "",
        database: str = "",
        path: str = "",
        echo_sql: bool = False,
        auto_create_tables: bool = True,
    ):
        """通过参数添加数据库配置"""
        if db_type.lower() == "sqlite":
            database_url = f"sqlite+aiosqlite:///{path or './test.db'}"
        elif db_type.lower() == "mysql":
            port = port or 3306
            database_url = f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        elif db_type.lower() == "postgresql":
            port = port or 5432
            database_url = f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")

        config = DatabaseConfig(
            name=name,
            database_url=database_url,
            echo_sql=echo_sql,
            auto_create_tables=auto_create_tables,
        )
        self.add_database(config)
