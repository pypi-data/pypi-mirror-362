from abc import ABC, abstractmethod
from typing import List, Tuple, Union, Optional
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

    def _response_language(self) -> str:
        if self.language is None:
            return ""

        return f"Respond in the {self.language} language."

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

    def generate_questions(self, **kwargs) -> List[str]:
        """

        """
        question_sql = self.get_similar_question_sql(question="", **kwargs)

        return [q["question"] for q in question_sql]

    def generate_followup_questions(
        self, question: str, sql: str, df: pd.DataFrame, n_questions: int = 5, **kwargs
    ) -> list:

        message_log = [
            self.system_message(
                f"You are a helpful data assistant. The user asked the question: '{question}'\n\nThe SQL query for this question was: {sql}\n\nThe following is a pandas DataFrame with the results of the query: \n{df.head(25).to_markdown()}\n\n"
            ),
            self.user_message(
                f"Generate a list of {n_questions} followup questions that the user might ask about this data. Respond with a list of questions, one per line. Do not answer with any explanations -- just the questions. Remember that there should be an unambiguous SQL query that can be generated from the question. Prefer questions that are answerable outside of the context of this conversation. Prefer questions that are slight modifications of the SQL query that was generated that allow digging deeper into the data. Each question will be turned into a button that the user can click to generate a new SQL query so don't use 'example' type questions. Each question must have a one-to-one correspondence with an instantiated SQL query." +
                self._response_language()
            ),
        ]

        llm_response = self.submit_prompt(message_log, **kwargs)

        numbers_removed = re.sub(r"^\d+\.\s*", "", llm_response, flags=re.MULTILINE)
        return numbers_removed.split("\n")

    @abstractmethod
    def run_sql(self, sql: str, params: Optional[tuple] = None) -> Optional[List[Dict[str, Any]]]:
        """
        运行 SQL 查询并返回结果
        """
        pass

    def _sanitize_plotly_code(self, raw_plotly_code: str) -> str:
        # Remove the fig.show() statement from the plotly code
        plotly_code = raw_plotly_code.replace("fig.show()", "")

        return plotly_code

    def _extract_python_code(self, markdown_string: str) -> str:
        # Strip whitespace to avoid indentation errors in LLM-generated code
        markdown_string = markdown_string.strip()

        # Regex pattern to match Python code blocks
        pattern = r"```[\w\s]*python\n([\s\S]*?)```|```([\s\S]*?)```"

        # Find all matches in the markdown string
        matches = re.findall(pattern, markdown_string, re.IGNORECASE)

        # Extract the Python code from the matches
        python_code = []
        for match in matches:
            python = match[0] if match[0] else match[1]
            python_code.append(python.strip())

        if len(python_code) == 0:
            return markdown_string

        return python_code[0]

    def generate_plotly_code(
        self, question: str = None, sql: str = None, df_metadata: str = None, **kwargs
    ) -> str:
        if question is not None:
            system_msg = f"The following is a pandas DataFrame that contains the results of the query that answers the question the user asked: '{question}'"
        else:
            system_msg = "The following is a pandas DataFrame "

        if sql is not None:
            system_msg += f"\n\nThe DataFrame was produced using this query: {sql}\n\n"

        system_msg += f"The following is information about the resulting pandas DataFrame 'df': \n{df_metadata}"

        message_log = [
            self.system_message(system_msg),
            self.user_message(
                "Can you generate the Python plotly code to chart the results of the dataframe? Assume the data is in a pandas dataframe called 'df'. If there is only one value in the dataframe, use an Indicator. Respond with only Python code. Do not answer with any explanations -- just the code."
            ),
        ]

        plotly_code = self.submit_prompt(message_log, kwargs=kwargs)

        return self._sanitize_plotly_code(self._extract_python_code(plotly_code))

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

    def get_plotly_figure(
        self, plotly_code: str, df: pd.DataFrame, dark_mode: bool = True
    ) -> plotly.graph_objs.Figure:

        ldict = {"df": df, "px": px, "go": go}
        try:
            exec(plotly_code, globals(), ldict)

            fig = ldict.get("fig", None)
        except Exception as e:
            # Inspect data types
            numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
            categorical_cols = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            # Decision-making for plot type
            if len(numeric_cols) >= 2:
                # Use the first two numeric columns for a scatter plot
                fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
            elif len(numeric_cols) == 1 and len(categorical_cols) >= 1:
                # Use a bar plot if there's one numeric and one categorical column
                fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0])
            elif len(categorical_cols) >= 1 and df[categorical_cols[0]].nunique() < 10:
                # Use a pie chart for categorical data with fewer unique values
                fig = px.pie(df, names=categorical_cols[0])
            else:
                # Default to a simple line plot if above conditions are not met
                fig = px.line(df)

        if fig is None:
            return None

        if dark_mode:
            fig.update_layout(template="plotly_dark")

        return fig

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