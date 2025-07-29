import os
from dotenv import load_dotenv
from lingua_sql.database.mysql_connector import MySQLConnector
from lingua_sql import LinguaSQL

# 加载环境变量
load_dotenv()

# 初始化数据库连接
db = MySQLConnector(
    host="172.22.182.17",
    user="root",
    password="O.-47Tz?",
    database="auto_form_filling"
)

# 连接数据库
db.connect()

try:
    # 获取所有表名
    tables = db.get_all_tables()
    print("\n数据库中的表:")
    for table in tables:
        print(f"- {table}")

    # 获取每个表的结构
    for table in tables:
        print(f"\n表 {table} 的结构:")
        schema = db.get_table_schema(table)
        for column in schema:
            print(f"- {column['COLUMN_NAME']}: {column['DATA_TYPE']} "
                  f"({'NULL' if column['IS_NULLABLE'] == 'YES' else 'NOT NULL'}) "
                  f"({column['COLUMN_COMMENT'] or '无注释'})")

    # 初始化 lingua_sql
    nl = LinguaSQL(config={
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "deepseek-chat",
        "client": "persistent"
    })

    # 为每个表生成 DDL
    for table in tables:
        schema = db.get_table_schema(table)
        ddl = f"CREATE TABLE {table} (\n"
        columns = []
        for column in schema:
            col_def = f"{column['COLUMN_NAME']} {column['DATA_TYPE']}"
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
        nl.train(ddl=ddl)
        print(f"\n已添加表 {table} 的 DDL 到 NLPipe")

    # 示例查询
    question = "查询所有表的结构"
    sql = nl.ask(question)
    print(f"\n问题: {question}")
    print(f"生成的 SQL: {sql}")

except Exception as e:
    print(f"发生错误: {e}")

finally:
    # 关闭数据库连接
    db.disconnect() 