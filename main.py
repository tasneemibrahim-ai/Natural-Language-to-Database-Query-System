import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from db_setup import setup_database, get_schema
from chains import build_sql_chain
from utils import extract_sql, validate_sql, execute_sql

load_dotenv()


def get_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")
    return ChatGroq(
        model="llama3-8b-8192",
        temperature=0.0,
        groq_api_key=api_key,
    )


def query_to_sql(question: str) -> dict:
    """Returns dict with keys: sql, dataframe, error."""
    try:
        llm = get_llm()
    except ValueError as e:
        return {"sql": None, "dataframe": None, "error": str(e)}

    db_path = setup_database()
    schema = get_schema()
    chain = build_sql_chain(llm)

    try:
        raw = chain.invoke({"schema": schema, "question": question})
    except Exception as e:
        return {"sql": None, "dataframe": None, "error": f"LLM error: {e}"}

    sql = extract_sql(raw)
    valid, err = validate_sql(sql)
    if not valid:
        return {"sql": sql, "dataframe": None, "error": err}

    df, exec_err = execute_sql(db_path, sql)
    if exec_err:
        return {"sql": sql, "dataframe": None, "error": f"Execution error: {exec_err}"}

    return {"sql": sql, "dataframe": df, "error": None}


if __name__ == "__main__":
    import sys
    user_q = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else input("Enter your database question (or press Enter for default): ").strip()
    q = user_q if user_q else "Show me all users from New York"
    print(f"\nQuestion: {q}")
    result = query_to_sql(q)
    print("\nGenerated SQL:")
    print(result["sql"])
    if result["error"]:
        print(f"\n❌ Error: {result['error']}")
    elif result["dataframe"] is not None:
        print(f"\n📊 Results ({len(result['dataframe'])} row(s)):")
        print(result["dataframe"].to_string(index=False))
