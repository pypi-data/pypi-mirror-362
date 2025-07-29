import mysql.connector
from mysql.connector import Error
from typing import Optional, List, Dict, Any

class MySQLConnector:
    def __init__(self, host, user, password, database):
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
        results = self.execute_query(query, (self.database,))
        return [row['TABLE_NAME'] for row in results] if results else []

    def __del__(self):
        """析构函数，确保关闭数据库连接"""
        self.disconnect() 