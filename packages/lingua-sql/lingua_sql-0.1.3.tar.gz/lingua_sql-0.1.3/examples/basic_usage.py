import os
from dotenv import load_dotenv
from lingua_sql import LinguaSQL

# 加载环境变量
load_dotenv()

# 初始化 lingua_sql
nl = LinguaSQL(config={
    "api_key": os.getenv("DEEPSEEK_API_KEY"),
    "model": "deepseek-chat",
    "client": "in-memory"  # 使用内存存储，也可以使用 "persistent" 持久化存储
})

# 训练模型
# 1. 添加 DDL
nl.train(ddl="""
CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    created_at TIMESTAMP
);

CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT,
    amount DECIMAL(10,2),
    created_at TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
""")

# 2. 添加示例问题和 SQL
nl.train(
    question="查询最近注册的 5 个客户",
    sql="SELECT name, email, created_at FROM customers ORDER BY created_at DESC LIMIT 5;"
)

nl.train(
    question="查询每个客户的总订单金额",
    sql="""
    SELECT 
        c.name,
        SUM(o.amount) as total_amount
    FROM customers c
    LEFT JOIN orders o ON c.id = o.customer_id
    GROUP BY c.id, c.name
    ORDER BY total_amount DESC;
    """
)

# 3. 添加文档
nl.train(documentation="""
客户表(customers)包含以下字段：
- id: 客户ID，主键
- name: 客户名称
- email: 客户邮箱
- created_at: 客户注册时间

订单表(orders)包含以下字段：
- id: 订单ID，主键
- customer_id: 客户ID，外键关联customers表
- amount: 订单金额
- created_at: 订单创建时间
""")

# 提问
question = "查询订单金额最高的前 3 个客户"
sql = nl.ask(question)
print(f"问题: {question}")
print(f"生成的 SQL: {sql}")

# 获取训练数据
training_data = nl.get_training_data()
print("\n训练数据:")
print(training_data) 