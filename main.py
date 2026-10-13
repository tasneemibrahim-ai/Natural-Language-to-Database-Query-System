from sql_chain import generate_sql
from db import get_connection

def run():
    question = input("Ask your question: ")

    sql_query = generate_sql(question)
    print("\nGenerated SQL:", sql_query)

    if any(word in sql_query.lower() for word in ["drop", "delete", "update"]):
        print("Unsafe query blocked!")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        print("\nResults:", results)
    except Exception as e:
        print("Query Error:", e)

if __name__ == "__main__":
    run()