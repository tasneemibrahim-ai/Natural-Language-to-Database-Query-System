from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

schema = """
Tables:
customers(id, name, city)
orders(id, customer_id, amount)
"""

prompt = PromptTemplate(
    template="""
You are an expert SQL generator.

Database Schema:
{schema}

Task:
Convert the natural language question into a SAFE SQL query.

Rules:
- ONLY generate SELECT queries
- DO NOT use DELETE, UPDATE, DROP, INSERT
- Use correct table relationships
- If the question is ambiguous, make a reasonable assumption

Question:
{question}

Return ONLY the SQL query (no explanation).
""",
    input_variables=["question"],
    partial_variables={"schema": schema}
)

def generate_sql(question):
    chain = prompt | llm
    response = chain.invoke({"question": question}).content.strip()

    # Clean output (sometimes wrapped in ```sql)
    if "```" in response:
        response = response.split("```")[1].replace("sql", "").strip()

    return response