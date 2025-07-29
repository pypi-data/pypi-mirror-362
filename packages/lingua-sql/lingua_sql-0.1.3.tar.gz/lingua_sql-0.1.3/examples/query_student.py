import os
from dotenv import load_dotenv
from lingua_sql import LinguaSQL

# 加载环境变量
load_dotenv()

try:
    # 初始化 lingua_sql，使用持久化存储
    nl = LinguaSQL(config={
        "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "deepseek-chat",
        "client": "persistent"
    })

    # 提问
    question = "学号为2023213203的学生的姓名为多少？"
    print(f"\n问题: {question}")
    
    # 获取查询结果
    results = nl.ask(question)
    
    # 打印结果
    if results:
        print("\n查询结果:")
        for row in results:
            print(row)
    else:
        print("\n未找到结果")

except Exception as e:
    print(f"发生错误: {e}") 