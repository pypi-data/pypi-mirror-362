from abc import ABC, abstractmethod
from typing import List, Tuple, Union
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import sqlparse

class Lingua_sqlBase(ABC):
    def __init__(self, config=None):
        if config is None:
            config = {}
        self.config = config
        self.run_sql_is_set = False
        self.static_documentation = ""
        self.dialect = self.config.get("dialect", "SQL")
        self.language = self.config.get("language", None)
        self.max_tokens = self.config.get("max_tokens", 14000)

    def log(self, message: str, title: str = "Info"):
        print(f"{title}: {message}")

    def generate_sql(self, question: str, allow_llm_to_see_data=False, **kwargs) -> str:
        """
        使用 LLM 生成 SQL 查询
        """
        question_sql_list = self.get_similar_question_sql(question, **kwargs)
        ddl_list = self.get_related_ddl(question, **kwargs)
        doc_list = self.get_related_documentation(question, **kwargs)
        prompt = self.get_sql_prompt(
            question=question,
            question_sql_list=question_sql_list,
            ddl_list=ddl_list,
            doc_list=doc_list,
            **kwargs,
        )
        self.log(title="SQL Prompt", message=prompt)
        llm_response = self.submit_prompt(prompt, **kwargs)
        self.log(title="LLM Response", message=llm_response)
        return self.extract_sql(llm_response)

    def extract_sql(self, llm_response: str) -> str:
        """
        从 LLM 响应中提取 SQL 查询
        """
        import re
        # 匹配 CREATE TABLE ... AS SELECT
        sqls = re.findall(r"\bCREATE\s+TABLE\b.*?\bAS\b.*?;", llm_response, re.DOTALL | re.IGNORECASE)
        if sqls:
            return sqls[-1]

        # 匹配 WITH 子句
        sqls = re.findall(r"\bWITH\b .*?;", llm_response, re.DOTALL | re.IGNORECASE)
        if sqls:
            return sqls[-1]

        # 匹配 SELECT ... ;
        sqls = re.findall(r"\bSELECT\b .*?;", llm_response, re.DOTALL | re.IGNORECASE)
        if sqls:
            return sqls[-1]

        # 匹配 ```sql ... ``` 块
        sqls = re.findall(r"```sql\s*\n(.*?)```", llm_response, re.DOTALL | re.IGNORECASE)
        if sqls:
            return sqls[-1].strip()

        # 匹配任何 ``` ... ``` 代码块
        sqls = re.findall(r"```(.*?)```", llm_response, re.DOTALL | re.IGNORECASE)
        if sqls:
            return sqls[-1].strip()

        return llm_response

    def is_sql_valid(self, sql: str) -> bool:
        """
        检查 SQL 查询是否有效
        """
        parsed = sqlparse.parse(sql)
        for statement in parsed:
            if statement.get_type() == 'SELECT':
                return True
        return False

    @abstractmethod
    def generate_embedding(self, data: str, **kwargs) -> List[float]:
        """生成文本的嵌入向量"""
        pass

    @abstractmethod
    def get_similar_question_sql(self, question: str, **kwargs) -> list:
        """获取相似问题的 SQL"""
        pass

    @abstractmethod
    def get_related_ddl(self, question: str, **kwargs) -> list:
        """获取相关的 DDL"""
        pass

    @abstractmethod
    def get_related_documentation(self, question: str, **kwargs) -> list:
        """获取相关的文档"""
        pass

    @abstractmethod
    def add_question_sql(self, question: str, sql: str, **kwargs) -> str:
        """添加问题和 SQL 对"""
        pass

    @abstractmethod
    def add_ddl(self, ddl: str, **kwargs) -> str:
        """添加 DDL"""
        pass

    @abstractmethod
    def add_documentation(self, documentation: str, **kwargs) -> str:
        """添加文档"""
        pass

    @abstractmethod
    def get_training_data(self, **kwargs) -> pd.DataFrame:
        """获取训练数据"""
        pass

    @abstractmethod
    def remove_training_data(self, id: str, **kwargs) -> bool:
        """删除训练数据"""
        pass

    @abstractmethod
    def system_message(self, message: str) -> any:
        """系统消息"""
        pass

    @abstractmethod
    def user_message(self, message: str) -> any:
        """用户消息"""
        pass

    @abstractmethod
    def assistant_message(self, message: str) -> any:
        """助手消息"""
        pass

    @abstractmethod
    def submit_prompt(self, prompt, **kwargs) -> str:
        """提交提示到 LLM"""
        pass

    def get_sql_prompt(
        self,
        question: str,
        question_sql_list: list,
        ddl_list: list,
        doc_list: list,
        **kwargs,
    ) -> str:
        """
        生成 SQL 提示
        """
        # 将字典列表转换为字符串列表
        question_sql_str_list = []
        for item in question_sql_list:
            if isinstance(item, dict):
                question_sql_str_list.append(f"Question: {item['question']}\nSQL: {item['sql']}")
            else:
                question_sql_str_list.append(str(item))

        prompt = [
            self.system_message(
                "You are a SQL expert. You will be given a question and some context about the database schema. "
                "Your task is to generate a SQL query that answers the question. "
                "Only return the SQL query, nothing else."
            ),
            self.user_message(
                f"Question: {question}\n\n"
                f"Context:\n"
                f"DDL:\n{chr(10).join(ddl_list)}\n\n"
                f"Documentation:\n{chr(10).join(doc_list)}\n\n"
                f"Similar Questions and SQL:\n{chr(10).join(question_sql_str_list)}"
            ),
        ]
        return prompt 