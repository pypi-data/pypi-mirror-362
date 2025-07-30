# 通用多数据库REST API

基于SQLAlchemy Automap的通用多数据库REST API服务，支持动态多数据库连接和管理。

## 功能特性

- 🗄️ **多数据库支持**: 同时连接和管理多个数据库（SQLite、MySQL、PostgreSQL）
- 🔄 **动态数据库管理**: 运行时添加、移除数据库连接
- 📊 **自动表映射**: 基于SQLAlchemy Automap自动映射现有表结构
- 🚀 **动态表创建**: 通过API创建表和索引
- 📤 **文件上传**: 支持JSON Lines、CSV、Parquet、SQL文件批量导入
- 🔍 **复杂查询**: 支持多种条件查询操作符
- 📝 **完整CRUD**: 创建、读取、更新、删除操作
- 🔄 **UPSERT操作**: 支持Insert or Update (有则更新，无则插入)
- 🎯 **自动索引**: 可选的自动索引创建以提升查询性能
- 📋 **API文档**: 自动生成的API文档 (Swagger/OpenAPI)
- 🐳 **Docker支持**: 完整的容器化部署方案

## 目录

- [安装运行](#安装运行)
- [配置说明](#配置说明)
- [API使用说明](#api使用说明)
- [UPSERT功能](#upsert功能)
- [文件上传](#文件上传)
- [Docker部署](#docker部署)
- [查询操作符](#查询操作符)
- [使用示例](#使用示例)
- [技术架构](#技术架构)

## 安装运行

### 环境要求

- Python 3.8+
- SQLAlchemy 2.0+
- FastAPI
- Uvicorn

### 安装依赖

```bash
# 使用uv (推荐)
uv sync

# 或使用pip
pip install -r requirements.txt
```

### 文件上传功能依赖

文件上传功能需要额外的依赖包：

- `polars`: 用于高性能数据处理（替代pandas）
- `pyarrow`: 用于处理Parquet文件
- `python-multipart`: 用于FastAPI文件上传支持

### 启动服务

```bash
# 开发模式
python run.py

# 或直接运行
uvicorn whatever.main:app --host 0.0.0.0 --port 8000 --reload
```

服务启动后，访问 <http://localhost:8000> 查看API文档。

## 配置说明

### 环境变量配置

```bash
# 默认数据库连接（可选）
DATABASE_URL=sqlite:///./default.db

# 是否显示SQL语句
ECHO_SQL=false

# 多数据库配置（JSON格式）
MULTI_DB_CONFIG='{"db1": {"database_url": "sqlite:///./db1.db", "echo_sql": false}, "db2": {"database_url": "sqlite:///./db2.db"}}'
```

### 多数据库配置示例

通过环境变量 `MULTI_DB_CONFIG` 配置多个数据库：

```json
{
  "users_db": {
    "database_url": "sqlite:///./users.db",
    "echo_sql": false,
    "auto_create_tables": true
  },
  "products_db": {
    "database_url": "mysql+pymysql://user:pass@localhost:3306/products",
    "echo_sql": true
  },
  "analytics_db": {
    "database_url": "postgresql://user:pass@localhost:5432/analytics"
  },
  "_default": "users_db"
}
```

## API使用说明

### 数据库管理

#### 获取数据库列表

```bash
GET /databases
```

#### 添加新数据库

```bash
POST /databases
{
  "name": "new_db",
  "db_type": "sqlite",
  "path": "./new_database.db",
  "echo_sql": false,
  "auto_create_tables": true
}
```

#### 移除数据库

```bash
DELETE /databases/{db_name}
```

### 表管理

#### 获取指定数据库的表列表

```bash
GET /databases/{db_name}/tables
```

#### 创建表

```bash
POST /databases/{db_name}/tables
{
  "table_name": "users",
  "columns": {
    "name": {"type": "string", "length": 100, "nullable": false},
    "email": {"type": "string", "length": 255, "nullable": false},
    "age": {"type": "integer", "nullable": true},
    "created_at": {"type": "datetime", "nullable": true}
  }
}
```

#### 获取表结构

```bash
GET /databases/{db_name}/tables/{table_name}/schema
```

#### 删除表

```bash
DELETE /databases/{db_name}/tables/{table_name}
```

### 数据操作

#### 查询数据

```bash
# 获取所有记录
GET /databases/{db_name}/tables/{table_name}

# 条件查询
GET /databases/{db_name}/tables/{table_name}?age__gt=25&name__like=张

# 分页查询
GET /databases/{db_name}/tables/{table_name}?limit=10&offset=20

# 自动创建索引
GET /databases/{db_name}/tables/{table_name}?age__gt=20&auto_index=true
```

#### 插入数据

```bash
POST /databases/{db_name}/tables/{table_name}
{
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

#### 更新数据

```bash
PUT /databases/{db_name}/tables/{table_name}/{record_id}
{
  "age": 26,
  "email": "new_email@example.com"
}
```

#### 删除数据

```bash
DELETE /databases/{db_name}/tables/{table_name}/{record_id}
```

### 索引管理

#### 创建索引

```bash
POST /databases/{db_name}/tables/{table_name}/indexes
{
  "index_name": "idx_users_email",
  "columns": ["email"],
  "unique": true
}
```

## UPSERT功能

### 功能概述

UPSERT操作可以在指定的唯一键或主键发生冲突时更新现有记录，否则插入新记录。这在需要"有则更新，无则插入"的场景中非常有用。

### 接口设计

为了符合RESTful设计原则，我们使用HTTP PATCH方法实现UPSERT功能：

```
PATCH /databases/{db_name}/tables/{table_name}/
```

**为什么使用PATCH？**

- PATCH语义上就是"部分更新或创建"，完美契合UPSERT的需求
- 区别于POST的纯创建语义和PUT的完整替换语义
- 符合RESTful设计原则

### 基础用法

#### 简单UPSERT（使用默认主键）

```bash
# 第一次调用：插入新记录
curl -X PATCH "http://localhost:8000/databases/default/tables/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com",
      "age": 25
    }
  }'

# 第二次调用：更新现有记录
curl -X PATCH "http://localhost:8000/databases/default/tables/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "id": 1,
      "name": "张三",
      "email": "zhangsan@example.com",
      "age": 26
    }
  }'
```

#### 高级UPSERT配置

```bash
curl -X PATCH "http://localhost:8000/databases/default/tables/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "email": "lisi@example.com",
      "name": "李四",
      "age": 30,
      "created_at": "2024-01-15T10:00:00Z"
    },
    "conflict_columns": ["email"],
    "update_columns": ["name", "age"],
    "insert_only_columns": ["created_at"]
  }'
```

### 参数说明

- **data**: 要插入或更新的数据（必需）
- **conflict_columns**: 冲突检测列，不指定则使用主键
- **update_columns**: 发生冲突时要更新的列，不指定则更新除冲突列外的所有列
- **insert_only_columns**: 仅在插入时设置的列（如created_at时间戳）

### 响应格式

```json
{
  "success": true,
  "action": "insert", // 或 "update"
  "message": "新记录已插入", // 或 "记录已更新，共更新 2 个字段"
  "database": "default",
  "table": "users",
  "data": {
    "id": 1,
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25
  },
  "affected_rows": 1
}
```

### UPSERT使用场景

#### 1. 用户信息同步

```bash
# 同步用户信息，存在则更新，不存在则创建
curl -X PATCH "http://localhost:8000/databases/default/tables/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "external_id": "ext_123",
      "name": "John Doe",
      "email": "john@example.com",
      "last_sync": "2024-01-15T15:30:00Z"
    },
    "conflict_columns": ["external_id"],
    "update_columns": ["name", "email", "last_sync"]
  }'
```

#### 2. 计数器更新

```bash
# 更新统计数据，如果记录不存在则初始化
curl -X PATCH "http://localhost:8000/databases/default/tables/counters/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "counter_name": "page_views",
      "value": 1,
      "created_at": "2024-01-15T15:30:00Z"
    },
    "conflict_columns": ["counter_name"],
    "update_columns": ["value"],
    "insert_only_columns": ["created_at"]
  }'
```

#### 3. 配置管理

```bash
# 更新应用配置，不存在则使用默认值
curl -X PATCH "http://localhost:8000/databases/default/tables/settings/" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "key": "theme",
      "value": "dark",
      "updated_at": "2024-01-15T15:30:00Z",
      "created_at": "2024-01-15T15:30:00Z"
    },
    "conflict_columns": ["key"],
    "update_columns": ["value", "updated_at"],
    "insert_only_columns": ["created_at"]
  }'
```

## 文件上传

### 支持的文件格式

- **JSON Lines (.jsonl, .ndjson)**: 每行一个JSON对象
- **CSV (.csv)**: 带表头的CSV文件
- **Parquet (.parquet)**: Parquet列式存储格式
- **SQL (.sql)**: SQL脚本文件

### 上传文件接口

```bash
POST /databases/{db_name}/upload/
```

使用multipart/form-data格式，支持以下参数：

| 参数              | 类型    | 必填 | 默认值 | 说明                                      |
| ----------------- | ------- | ---- | ------ | ----------------------------------------- |
| file              | file    | 是   | -      | 要上传的文件                              |
| table_name        | string  | 是   | -      | 目标表名                                  |
| create_table      | boolean | 否   | true   | 如果表不存在是否自动创建                  |
| if_exists         | string  | 否   | append | 表已存在时的处理方式：append/replace/fail |
| batch_size        | integer | 否   | 1000   | 批量插入大小                              |
| encoding          | string  | 否   | utf-8  | 文件编码                                  |
| csv_delimiter     | string  | 否   | ,      | CSV分隔符                                 |
| csv_quote_char    | string  | 否   | "      | CSV引用字符                               |
| sql_batch_execute | boolean | 否   | true   | 是否批量执行SQL语句                       |

### 文件上传示例

**上传JSON Lines文件：**

```bash
curl -X POST "http://localhost:8000/databases/default/upload/" \
  -F "file=@employees.jsonl" \
  -F "table_name=employees" \
  -F "create_table=true" \
  -F "if_exists=replace"
```

**上传CSV文件：**

```bash
curl -X POST "http://localhost:8000/databases/default/upload/" \
  -F "file=@products.csv" \
  -F "table_name=products" \
  -F "csv_delimiter=," \
  -F "encoding=utf-8"
```

**上传Parquet文件：**

```bash
curl -X POST "http://localhost:8000/databases/default/upload/" \
  -F "file=@orders.parquet" \
  -F "table_name=orders" \
  -F "create_table=true"
```

**上传SQL文件：**

```bash
curl -X POST "http://localhost:8000/databases/default/upload/" \
  -F "file=@schema.sql" \
  -F "table_name=temp" \
  -F "sql_batch_execute=false"
```

### 获取支持的文件格式信息

```bash
GET /databases/{db_name}/upload/formats
```

### 快速开始示例

运行文件上传示例脚本：

```bash
# 启动API服务
python run.py

# 在另一个终端运行示例
python example_upload.py
```

或使用完整测试脚本：

```bash
python test_upload.py
```

## Docker部署

本项目提供了完整的 Docker 容器化解决方案，包含应用服务、MySQL 数据库和 phpMyAdmin 管理界面。

### 快速开始

#### 生产环境部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

#### 开发环境部署

```bash
# 使用开发配置启动（支持代码热重载）
docker-compose -f docker-compose.dev.yml up -d

# 查看应用日志
docker-compose -f docker-compose.dev.yml logs -f app
```

### 服务说明

#### 端口映射

- **应用服务**: <http://localhost:8000>

  - API 文档: <http://localhost:8000/docs>
  - ReDoc 文档: <http://localhost:8000/redoc>

- **phpMyAdmin**: <http://localhost:8080>

  - 用户名: root
  - 密码: whatever123

- **MySQL**: localhost:3306

  - 数据库: whatever_db
  - 用户名: root / whatever_user
  - 密码: whatever123

- **Redis** (仅开发环境): localhost:6379

#### 数据卷

- `mysql_data` / `mysql_dev_data`: MySQL 数据持久化
- `redis_data`: Redis 数据持久化（开发环境）
- `./uploads`: 文件上传目录

### Docker环境变量

可以通过 `.env` 文件或环境变量配置：

```bash
# 数据库连接
DATABASE_URL=mysql+aiomysql://root:whatever123@mysql:3306/whatever_db

# SQL 日志
ECHO_SQL=false

# 自动建表
AUTO_CREATE_TABLES=true

# MySQL 配置
MYSQL_ROOT_PASSWORD=whatever123
MYSQL_DATABASE=whatever_db
MYSQL_USER=whatever_user
MYSQL_PASSWORD=whatever123
```

### 常用Docker命令

#### 服务管理

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v

# 重建应用镜像
docker-compose build app

# 只启动特定服务
docker-compose up -d mysql
```

#### 数据库操作

```bash
# 连接 MySQL
docker-compose exec mysql mysql -u root -p

# 导出数据库
docker-compose exec mysql mysqldump -u root -pwhatever123 whatever_db > backup.sql

# 导入数据库
docker-compose exec -T mysql mysql -u root -pwhatever123 whatever_db < backup.sql

# 查看 MySQL 日志
docker-compose logs mysql
```

#### 应用调试

```bash
# 查看应用日志
docker-compose logs -f app

# 进入应用容器
docker-compose exec app bash

# 重启应用服务
docker-compose restart app
```

### Docker自定义配置

#### MySQL 配置

编辑 `docker/mysql/conf.d/custom.cnf` 文件来自定义 MySQL 配置。

#### 应用配置

编辑 `docker-compose.yml` 中的环境变量或创建 `.env` 文件。

#### 初始化数据

编辑 `docker/mysql/init.sql` 文件来添加初始化 SQL 脚本。

### 性能优化

#### 生产环境优化

1. 调整 MySQL 内存配置
2. 使用外部 Redis 缓存
3. 配置 nginx 反向代理
4. 启用 MySQL 慢查询日志

#### 开发环境优化

1. 使用代码热重载
2. 启用 SQL 日志调试
3. 使用本地缓存

### Docker故障排除

#### 常见问题

1. **MySQL 连接失败**

   ```bash
   # 检查 MySQL 健康状态
   docker-compose exec mysql mysqladmin ping -u root -p
   ```

2. **应用启动失败**

   ```bash
   # 查看详细日志
   docker-compose logs app
   ```

3. **端口冲突**

   ```bash
   # 修改 docker-compose.yml 中的端口映射
   ports:
     - "8001:8000"  # 修改本地端口
   ```

4. **数据卷权限问题**

   ```bash
   # 修复权限
   sudo chown -R $USER:$USER uploads/
   ```

#### 监控和日志

```bash
# 查看所有服务日志
docker-compose logs

# 实时跟踪特定服务日志
docker-compose logs -f mysql

# 查看最近的日志
docker-compose logs --tail=100 app

# 查看资源使用情况
docker stats
```

## 查询操作符

支持的查询操作符：

- `=` 或 `column=value`: 等于
- `column__gt=value`: 大于
- `column__gte=value`: 大于等于
- `column__lt=value`: 小于
- `column__lte=value`: 小于等于
- `column__like=value`: 模糊匹配
- `column__in=value1,value2`: 包含于列表
- `column__between=value1,value2`: 范围查询

## 支持的数据类型

- `string`: 字符串类型
- `integer`: 整数类型
- `float`: 浮点数类型
- `boolean`: 布尔类型
- `datetime`: 日期时间类型
- `text`: 长文本类型

## 使用示例

### Python客户端示例

```python
import requests

base_url = "http://localhost:8000"

# 1. 添加新数据库
db_config = {
    "name": "my_app_db",
    "db_type": "sqlite",
    "path": "./my_app.db"
}
response = requests.post(f"{base_url}/databases", json=db_config)
print(response.json())

# 2. 创建表
table_config = {
    "table_name": "users",
    "columns": {
        "name": {"type": "string", "length": 100, "nullable": False},
        "email": {"type": "string", "length": 255, "nullable": False},
        "age": {"type": "integer", "nullable": True}
    }
}
response = requests.post(f"{base_url}/databases/my_app_db/tables", json=table_config)

# 3. 插入数据
user_data = {"name": "张三", "email": "zhangsan@test.com", "age": 25}
response = requests.post(f"{base_url}/databases/my_app_db/tables/users", json=user_data)

# 4. 查询数据
response = requests.get(f"{base_url}/databases/my_app_db/tables/users?age__gt=20")
users = response.json()["data"]

# 5. UPSERT操作
upsert_data = {
    "data": {
        "email": "zhangsan@test.com",
        "name": "张三（更新）",
        "age": 26
    },
    "conflict_columns": ["email"],
    "update_columns": ["name", "age"]
}
response = requests.patch(f"{base_url}/databases/my_app_db/tables/users/", json=upsert_data)
```

### curl示例

```bash
# 添加数据库
curl -X POST "http://localhost:8000/databases" \
  -H "Content-Type: application/json" \
  -d '{"name": "test_db", "db_type": "sqlite", "path": "./test.db"}'

# 创建表
curl -X POST "http://localhost:8000/databases/test_db/tables" \
  -H "Content-Type: application/json" \
  -d '{"table_name": "products", "columns": {"name": {"type": "string"}, "price": {"type": "float"}}}'

# 插入数据
curl -X POST "http://localhost:8000/databases/test_db/tables/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "笔记本电脑", "price": 5999.99}'

# 查询数据
curl "http://localhost:8000/databases/test_db/tables/products?price__gt=1000"

# UPSERT操作
curl -X PATCH "http://localhost:8000/databases/test_db/tables/products/" \
  -H "Content-Type: application/json" \
  -d '{"data": {"name": "笔记本电脑", "price": 5599.99}, "conflict_columns": ["name"]}'
```

## 测试

运行测试脚本：

```bash
# 确保服务正在运行
python run.py

# 在另一个终端运行测试
python test_api.py
```

## 技术架构

- **FastAPI**: 现代Web框架，自动生成API文档
- **SQLAlchemy**: Python SQL工具包和ORM
- **Automap**: 自动映射现有数据库表结构
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI服务器
- **Polars**: 高性能数据处理（用于文件上传）
- **Docker**: 容器化部署

## 注意事项

1. **数据库连接**: 确保目标数据库服务正在运行且可访问
2. **权限要求**: 确保有足够的数据库权限执行DDL和DML操作
3. **主键字段**: 创建表时如果没有指定主键，会自动添加`id`字段作为主键
4. **数据类型**: 不同数据库的类型支持可能有差异
5. **并发访问**: 生产环境建议配置连接池和适当的并发设置
6. **UPSERT性能**: UPSERT操作会先执行查询再决定插入或更新，确保冲突检测列上有适当的索引
7. **文件上传**: 大文件上传时注意内存使用，建议使用分批处理

## 最佳实践

### UPSERT最佳实践

1. **明确指定冲突检测列**: 不要依赖默认主键，明确指定业务相关的唯一键
2. **合理使用insert_only_columns**: 对于时间戳字段，使用insert_only_columns避免意外更新
3. **精确控制更新字段**: 使用update_columns明确指定哪些字段可以更新
4. **错误处理**: 在客户端代码中妥善处理各种错误情况

### 性能优化

1. **索引优化**: 为常用查询字段创建合适的索引
2. **批量操作**: 使用文件上传功能进行批量数据导入
3. **连接池**: 生产环境配置合适的数据库连接池
4. **缓存策略**: 对于频繁查询的数据考虑使用缓存

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License
