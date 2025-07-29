# Lingua SQL

一个基于 DeepSeek 和 ChromaDB 的文本转 SQL（Text-to-SQL）流水线工具。

## 项目简介
Lingua SQL 旨在帮助用户通过自然语言问题自动生成 SQL 查询，支持自定义训练、数据库结构导入、示例问答训练等，适用于数据分析、智能问答等场景。

## 主要功能
- 支持 DeepSeek、OpenAI 等大模型 API
- 支持 ChromaDB 作为向量数据库
- 支持 MySQL 数据库结构自动导入
- 支持自定义 DDL、示例问答、文档训练
- 支持持久化和内存两种存储方式
- 提供丰富的训练与推理接口

## 安装方法

建议使用 Python 3.8 及以上版本。

```bash
pip install -r requirements.txt
```
或使用 `pyproject.toml` 进行依赖管理。

## 快速开始

### 1. 基本用法
```python
import os
from dotenv import load_dotenv
from lingua_sql import LinguaSQL

# 加载环境变量
load_dotenv()

# 初始化 lingua_sql
nl = LinguaSQL(config={
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "model": "deepseek-chat",
    "client": "in-memory"  # 可选 "persistent"
})

# 添加 DDL
nl.train(ddl="""
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
);
""")

# 添加示例问答
nl.train(
    question="查询最近注册的5个客户",
    sql="SELECT name, email, created_at FROM customers ORDER BY created_at DESC LIMIT 5;"
)

# 生成 SQL
question = "查询订单金额最高的前3个客户"
sql = nl.ask(question)
print(f"问题: {question}")
print(f"生成的 SQL: {sql}")
```

### 2. 数据库结构自动导入
```python
from lingua_sql.database.mysql_connector import MySQLConnector

# 初始化数据库连接
conn = MySQLConnector(
    host="localhost",
    user="root",
    password="your_password",
    database="your_db"
)
conn.connect()

# 获取所有表结构并导入
for table in conn.get_all_tables():
    ddl = ... # 参见 examples/database_usage.py
    nl.train(ddl=ddl)
conn.disconnect()
```

更多用法请参考 `examples/` 目录。

## 联系方式
作者：殷旭  
邮箱：2337302325@qq.com

## 许可证
MIT License 

cd lingua_sql
git init
git remote add origin git@github.com:4869-yinxu/lingua_sql.git

git add .
git commit -m "Release version 0.1.3"
git tag v0.1.3
git push origin main
git push origin v0.1.3