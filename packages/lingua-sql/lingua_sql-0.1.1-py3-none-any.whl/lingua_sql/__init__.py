from .chromadb.chromadb_vector import ChromaDBVectorStore
from .deepseek.deepseek_chat import DeepSeekChat
from .database.mysql_connector import MySQLConnector

class LinguaSQL(ChromaDBVectorStore, DeepSeekChat):
    def __init__(self, config=None):
        if config is None:
            config = {}
        ChromaDBVectorStore.__init__(self, config=config)
        DeepSeekChat.__init__(self, config=config)
        
        # 初始化数据库连接
        self.db = MySQLConnector(
            host=config.get("db_host"),
            user=config.get("db_user"),
            password=config.get("db_password"),
            database=config.get("db_database")
        )
        self.db.connect()

        # 新增：根据config参数决定是否自动导入schema
        if config.get("import_schema_on_init", False):
            print("正在从数据库导入表结构...")
            self.import_database_schema()

    def train(self, question=None, sql=None, ddl=None, documentation=None, **kwargs):
        """训练模型"""
        if question and sql:
            self.add_question_sql(question, sql, **kwargs)
        if ddl:
            self.add_ddl(ddl, **kwargs)
        if documentation:
            self.add_documentation(documentation, **kwargs)

    def import_database_schema(self):
        """从数据库导入所有表的 DDL 到 ChromaDB"""
        try:
            # 检查是否已经导入过 DDL
            if self.ddl_collection.get(
                where={"type": "ddl_imported"},
                limit=1
            ):
                print("数据库表结构已经导入过，跳过导入步骤")
                return True

            # 获取所有表名
            tables = self.db.get_tables()
            
            # 为每个表生成 DDL
            for table in tables:
                schema = self.db.get_table_schema(table)
                ddl = f"CREATE TABLE {table} (\n"
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
                
                # 添加 DDL 到 lingua_sql
                self.train(ddl=ddl)
                print(f"\n已添加表 {table} 的 DDL 到 NLPipe")
            
            # 添加导入标记
            self.ddl_colle2510ction.add(
                documents=["DDL imported"],
                metadatas=[{"type": "ddl_imported"}],
                ids=["ddl_imported_marker"]
            )
            
            return True
        except Exception as e:
            print(f"导入数据库 schema 时发生错误: {e}")
            return False

    def ask(self, question: str, allow_llm_to_see_data: bool = False, **kwargs):
        """生成 SQL 并执行查询"""
        # 生成 SQL
        sql = self.generate_sql(question, allow_llm_to_see_data=allow_llm_to_see_data, **kwargs)
        print(f"\n生成的 SQL: {sql}")
        
        # 执行 SQL
        if sql:
            try:
                results = self.db.execute_query(sql)
                return results
            except Exception as e:
                print(f"执行 SQL 时发生错误: {e}")
                return None
        return None

    def __del__(self):
        """析构函数，确保关闭数据库连接"""
        if hasattr(self, 'db'):
            self.db.disconnect() 