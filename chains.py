from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

SQL_TEMPLATE = """You are an expert SQL assistant. Given a SQLite database with the following schema:

{schema}

Convert the natural language question below into a valid SQLite SELECT query.

Rules:
- Only generate SELECT statements.
- Never use DROP, DELETE, INSERT, UPDATE, ALTER, or TRUNCATE.
- Use proper SQLite syntax.
- Return ONLY the SQL query inside a ```sql code block — nothing else.

Question: {question}

SQL Query:"""


def build_sql_chain(llm):
    prompt = ChatPromptTemplate.from_template(SQL_TEMPLATE)
    return prompt | llm | StrOutputParser()
