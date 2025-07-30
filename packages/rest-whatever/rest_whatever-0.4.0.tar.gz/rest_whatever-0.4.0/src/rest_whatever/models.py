from typing import Any

from pydantic import BaseModel, Field


class TableCreateRequest(BaseModel):
    table_name: str = Field(..., description="表名")
    columns: dict[str, dict[str, Any]] = Field(..., description="列定义")


class IndexCreateRequest(BaseModel):
    index_name: str = Field(..., description="索引名")
    columns: list[str] = Field(..., description="索引列")
    unique: bool = Field(False, description="是否唯一索引")


class DatabaseAddRequest(BaseModel):
    name: str = Field(..., description="数据库名称")
    db_type: str = Field(..., description="数据库类型: sqlite, mysql, postgresql")
    host: str | None = Field("localhost", description="主机地址")
    port: int | None = Field(None, description="端口号")
    username: str | None = Field("", description="用户名")
    password: str | None = Field("", description="密码")
    database: str | None = Field("", description="数据库名")
    path: str | None = Field("", description="SQLite文件路径")
    echo_sql: bool = Field(False, description="是否显示SQL")
    auto_create_tables: bool = Field(True, description="是否自动创建表")


class QueryCondition(BaseModel):
    column: str
    operator: str = Field(..., description="操作符: eq, ne, gt, gte, lt, lte, like, in, between")
    value: str | int | float | list[Any] | None


class FileUploadRequest(BaseModel):
    """文件上传配置"""

    table_name: str = Field(..., description="目标表名")
    create_table: bool = Field(True, description="如果表不存在是否自动创建")
    if_exists: str = Field("append", description="表已存在时的处理方式: replace, append, fail")
    batch_size: int = Field(1000, description="批量插入大小")
    encoding: str = Field("utf-8", description="文件编码")

    # CSV特定选项
    csv_delimiter: str = Field(",", description="CSV分隔符")
    csv_quote_char: str = Field('"', description="CSV引用字符")

    # SQL特定选项
    sql_batch_execute: bool = Field(True, description="是否批量执行SQL语句")


class UploadResult(BaseModel):
    """上传结果"""

    success: bool
    message: str
    database: str
    table: str
    records_processed: int
    records_inserted: int
    records_failed: int
    execution_time: float
    errors: list[str] = []


class ColumnInfo(BaseModel):
    """表列信息"""

    name: str = Field(..., description="列名")
    is_primary_key: bool = Field(..., description="是否为主键")
    is_nullable: bool | None = Field(..., description="是否可为空")
    type: str = Field(..., description="列类型")
    detail: str = Field(..., description="列详细信息")


class IndexInfo(BaseModel):
    """索引信息"""

    name: str | None = Field(..., description="索引名")
    cols: list[str] = Field(..., description="索引列名列表")


class TableSchemaResponse(BaseModel):
    """表结构响应"""

    database: str = Field(..., description="数据库名")
    table_name: str = Field(..., description="表名")
    columns: list[ColumnInfo] = Field(..., description="列信息列表")
    indexes: list[IndexInfo] = Field(..., description="索引信息列表")
    primary_keys: list[str] = Field(..., description="主键列名列表")


class UpsertRequest(BaseModel):
    """插入或更新请求"""

    data: dict[str, Any] = Field(..., description="要插入或更新的数据")
    conflict_columns: list[str] | None = Field(None, description="冲突检测列（唯一键/主键），不指定则自动使用主键")
    update_columns: list[str] | None = Field(None, description="发生冲突时要更新的列，不指定则更新除冲突列外的所有列")
    insert_only_columns: list[str] | None = Field(None, description="仅在插入时设置的列（如created_at）")


class UpsertResponse(BaseModel):
    """插入或更新响应"""

    success: bool = Field(..., description="操作是否成功")
    action: str = Field(..., description="执行的操作: 'insert' 或 'update'")
    message: str = Field(..., description="操作结果消息")
    database: str = Field(..., description="数据库名")
    table: str = Field(..., description="表名")
    data: dict[str, Any] = Field(..., description="操作后的记录数据")
    affected_rows: int = Field(..., description="影响的行数")
