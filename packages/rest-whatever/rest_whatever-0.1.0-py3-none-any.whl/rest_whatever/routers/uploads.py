from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from rest_whatever.database import DatabaseManager
from rest_whatever.models import FileUploadRequest, UploadResult
from rest_whatever.utils import process_upload_file

router = APIRouter(prefix="/databases/{db_name}/upload", tags=["文件上传"])


def create_upload_router(db_manager: DatabaseManager):
    """创建文件上传路由"""

    @router.post("/", response_model=UploadResult)
    async def upload_file(
        db_name: str,
        file: UploadFile = File(..., description="要上传的文件"),
        table_name: str = Form(..., description="目标表名"),
        create_table: bool = Form(True, description="如果表不存在是否自动创建"),
        if_exists: str = Form("append", description="表已存在时的处理方式: replace, append, fail"),
        batch_size: int = Form(1000, description="批量插入大小"),
        encoding: str = Form("utf-8", description="文件编码"),
        csv_delimiter: str = Form(",", description="CSV分隔符"),
        csv_quote_char: str = Form('"', description="CSV引用字符"),
        sql_batch_execute: bool = Form(True, description="是否批量执行SQL语句"),
    ):
        """
        上传文件并导入到指定数据库表中

        支持的文件格式：
        - JSON Lines (.jsonl, .ndjson): 每行一个JSON对象
        - CSV (.csv): 带表头的CSV文件
        - Parquet (.parquet): Parquet格式文件
        - SQL (.sql): SQL脚本文件

        参数说明：
        - table_name: 目标表名
        - create_table: 如果表不存在是否自动创建
        - if_exists: 表已存在时的处理方式
          - append: 追加数据（默认）
          - replace: 替换表中所有数据
          - fail: 如果表有数据则失败
        - batch_size: 批量插入的记录数量
        - encoding: 文件编码格式
        - csv_delimiter: CSV文件的字段分隔符
        - csv_quote_char: CSV文件的引用字符
        - sql_batch_execute: SQL文件是否批量执行
        """

        # 验证数据库是否存在
        if db_name not in db_manager.list_databases():
            raise HTTPException(status_code=404, detail=f"数据库 '{db_name}' 不存在")

        # 验证if_exists参数
        if if_exists not in ["append", "replace", "fail"]:
            raise HTTPException(
                status_code=400,
                detail="if_exists参数必须是: append, replace, fail 中的一个",
            )

        # 验证文件类型
        if not file.filename:
            raise HTTPException(status_code=400, detail="文件名不能为空")

        file_extension = file.filename.lower().split(".")[-1]
        supported_formats = ["jsonl", "ndjson", "csv", "parquet", "sql"]

        if file_extension not in supported_formats:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件格式 '.{file_extension}'，支持的格式: {', '.join(['.' + f for f in supported_formats])}",
            )

        # 创建配置对象
        config = FileUploadRequest(
            table_name=table_name,
            create_table=create_table,
            if_exists=if_exists,
            batch_size=batch_size,
            encoding=encoding,
            csv_delimiter=csv_delimiter,
            csv_quote_char=csv_quote_char,
            sql_batch_execute=sql_batch_execute,
        )

        # 处理文件上传
        try:
            result = await process_upload_file(file, config, db_name, db_manager)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

    @router.get("/formats")
    async def get_supported_formats():
        """获取支持的文件格式信息"""
        return {
            "supported_formats": [
                {
                    "extension": ".jsonl / .ndjson",
                    "description": "JSON Lines格式，每行一个JSON对象",
                    "example": '{"name": "张三", "age": 25}\n{"name": "李四", "age": 30}',
                },
                {
                    "extension": ".csv",
                    "description": "CSV格式，第一行为表头",
                    "example": "name,age,email\n张三,25,zhangsan@example.com\n李四,30,lisi@example.com",
                },
                {
                    "extension": ".parquet",
                    "description": "Parquet列式存储格式",
                    "example": "二进制格式文件",
                },
                {
                    "extension": ".sql",
                    "description": "SQL脚本文件，包含CREATE TABLE、INSERT等语句",
                    "example": "CREATE TABLE users (id INT, name VARCHAR(100));\nINSERT INTO users VALUES (1, '张三');",
                },
            ],
            "encoding_options": ["utf-8", "gbk", "gb2312", "latin-1"],
            "if_exists_options": [
                {"value": "append", "description": "追加数据到现有表（默认）"},
                {"value": "replace", "description": "替换表中所有数据"},
                {"value": "fail", "description": "如果表已有数据则失败"},
            ],
        }

    return router
