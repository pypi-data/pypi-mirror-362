import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any
import pandas as pd
import re
from ..base.base import Lingua_sqlBase

class MySQLConnector(Lingua_sqlBase):
    def __init__(self, host, user, password, database, config=None):
        # Initialize the base class first
        super().__init__(config=config)

        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self) -> bool:
        """连接到 MySQL 数据库"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                if self.connection.is_connected():
                    print("数据库连接成功")
                    self.cursor = self.connection.cursor(dictionary=True)
                    return True
            return True
        except Error as e:
            print(f"连接数据库时发生错误: {e}")
            return False

    def disconnect(self) -> None:
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None
            if self.connection and self.connection.is_connected():
                self.connection.close()
                self.connection = None
                print("数据库连接已关闭")
        except Error as e:
            print(f"关闭数据库连接时发生错误: {e}")

    def run_sql(self, sql: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
        """执行 SQL 查询并返回结果"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"执行查询时发生错误: {e}")
            return None

    def execute_update(self, query: str, params: Optional[tuple] = None) -> int:
        """执行更新操作（INSERT, UPDATE, DELETE）"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.rowcount
        except Error as err:
            self.connection.rollback()
            print(f"更新执行失败: {err}")
            raise

    def get_tables(self) -> List[str]:
        """获取数据库中的所有表名"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return []
            self.cursor.execute("SHOW TABLES")
            tables = self.cursor.fetchall()
            return [list(table.values())[0] for table in tables]
        except Error as e:
            print(f"获取表名时发生错误: {e}")
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """获取指定表的结构信息"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return []
            self.cursor.execute(f"""
                SELECT 
                    COLUMN_NAME,
                    DATA_TYPE,
                    CHARACTER_MAXIMUM_LENGTH,
                    IS_NULLABLE,
                    COLUMN_KEY,
                    COLUMN_COMMENT
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = '{self.database}'
                AND TABLE_NAME = '{table_name}'
                ORDER BY ORDINAL_POSITION
            """)
            return self.cursor.fetchall()
        except Error as e:
            print(f"获取表 {table_name} 结构时发生错误: {e}")
            return []

    def get_all_tables(self) -> List[str]:
        """获取所有表名"""
        query = """
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_SCHEMA = %s
        """
        results = self.run_sql(query, (self.database,))
        return [row['TABLE_NAME'] for row in results] if results else []

    def generate_ddl_from_schema(self, table_name: str) -> str:
        """根据表结构生成DDL语句"""
        schema = self.get_table_schema(table_name)
        if not schema:
            return ""

        ddl = f"CREATE TABLE {table_name} (\n"
        columns = []
        for column in schema:
            col_def = f"    {column['COLUMN_NAME']} {column['DATA_TYPE']}"
            if column['CHARACTER_MAXIMUM_LENGTH']:
                col_def += f"({column['CHARACTER_MAXIMUM_LENGTH']})"
            if column['IS_NULLABLE'] == 'NO':
                col_def += " NOT NULL"
            if column['COLUMN_KEY'] == 'PRI':
                col_def += " PRIMARY KEY"
            columns.append(col_def)
        ddl += ",\n".join(columns)
        ddl += "\n);"

        return ddl

    def import_database_schema(self, ddl_collection, train_method):
        """从数据库导入所有表的 DDL 到向量数据库"""
        try:
            # 检查是否已经导入过 DDL
            if ddl_collection.get(
                where={"type": "ddl_imported"},
                limit=1
            ):
                print("数据库表结构已经导入过，跳过导入步骤")
                return True

            # 获取所有表名
            tables = self.get_tables()

            # 为每个表生成 DDL
            for table in tables:
                ddl = self.generate_ddl_from_schema(table)
                if ddl:
                    # 添加 DDL 到向量数据库
                    train_method(ddl=ddl)
                    print(f"\n已添加表 {table} 的 DDL 到向量数据库")

            # 添加导入标记
            ddl_collection.add(
                documents=["DDL imported"],
                metadatas=[{"type": "ddl_imported"}],
                ids=["ddl_imported_marker"]
            )

            return True
        except Exception as e:
            print(f"导入数据库 schema 时发生错误: {e}")
            return False

    def execute_sql_with_error_handling(self, sql: str, params: Optional[tuple] = None):
        """执行SQL并处理错误"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                print("数据库连接不可用，无法执行SQL")
                return None

        try:
            results = self.run_sql(sql, params)
            return results
        except Exception as e:
            print(f"执行 SQL 时发生错误: {e}")
            return None

    # Implementation of abstract methods from Lingua_sqlBase
    def generate_embedding(self, data: str, **kwargs) -> List[float]:
        """生成文本的嵌入向量 - 简单实现，实际应该使用embedding模型"""
        # 这是一个简单的占位符实现
        # 在实际使用中，应该使用真正的embedding模型
        return [0.0] * 384  # 返回384维的零向量作为占位符

    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        """获取相似问题的 SQL - 简单实现"""
        # 这是一个占位符实现，实际应该从向量数据库中检索
        return []

    def get_related_ddl(self, question: str, **kwargs) -> list:
        """获取相关的 DDL - 简单实现"""
        # 这是一个占位符实现，实际应该从向量数据库中检索
        return []

    def get_related_documentation(self, question: str, **kwargs) -> list:
        """获取相关的文档 - 简单实现"""
        # 这是一个占位符实现，实际应该从向量数据库中检索
        return []

    def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
        """添加问题和 SQL 对 - 简单实现"""
        # 这是一个占位符实现，实际应该添加到向量数据库
        return "mock_id"

    def add_ddl(self, ddl: str, **kwargs) -> str:
        """添加 DDL - 简单实现"""
        # 这是一个占位符实现，实际应该添加到向量数据库
        return "mock_id"

    def add_documentation(self, documentation: str, **kwargs) -> str:
        """添加文档 - 简单实现"""
        # 这是一个占位符实现，实际应该添加到向量数据库
        return "mock_id"

    def get_training_data(self, **kwargs) -> pd.DataFrame:
        """获取训练数据 - 简单实现"""
        # 返回空的DataFrame作为占位符
        return pd.DataFrame()

    def remove_training_data(self, id: str, **kwargs) -> bool:
        """删除训练数据 - 简单实现"""
        # 这是一个占位符实现
        return True

    def system_message(self, message: str) -> any:
        """系统消息 - 简单实现"""
        return {"role": "system", "content": message}

    def user_message(self, message: str) -> any:
        """用户消息 - 简单实现"""
        return {"role": "user", "content": message}

    def assistant_message(self, message: str) -> any:
        """助手消息 - 简单实现"""
        return {"role": "assistant", "content": message}

    def submit_prompt(self, prompt, **kwargs) -> str:
        """提交提示到 LLM - 简单实现"""
        # 这是一个占位符实现，实际应该调用LLM API
        if isinstance(prompt, list):
            # 如果是消息列表，提取最后一条用户消息
            for msg in reversed(prompt):
                if msg.get("role") == "user":
                    return f"Mock response for: {msg.get('content', '')}"
        elif isinstance(prompt, str):
            return f"Mock response for: {prompt}"
        return "Mock response"

    def get_sql_prompt(self, question: str, question_sql_list: list, ddl_list: list, doc_list: list, **kwargs) -> str:
        """生成SQL提示 - 简单实现"""
        prompt = f"Question: {question}\n\n"
        if question_sql_list:
            prompt += "Similar questions and SQL:\n"
            for item in question_sql_list:
                prompt += f"Q: {item.get('question', '')}\n"
                prompt += f"SQL: {item.get('sql', '')}\n\n"
        if ddl_list:
            prompt += "Related DDL:\n"
            for ddl in ddl_list:
                prompt += f"{ddl}\n\n"
        if doc_list:
            prompt += "Related documentation:\n"
            for doc in doc_list:
                prompt += f"{doc}\n\n"
        prompt += "Generate SQL for the question above."
        return prompt

    def __del__(self):
        """析构函数，确保关闭数据库连接"""
        self.disconnect() 