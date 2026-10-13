import streamlit as st
from sql_chain import generate_sql
from db import get_connection

st.set_page_config(page_title="Text-to-SQL System", layout="wide")

st.title("🧠 Natural Language to SQL System")

st.markdown("Ask questions about the database in plain English.")

question = st.text_input("Enter your question:")

if st.button("🚀 Generate & Execute"):

    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Generating SQL..."):

            try:
                sql_query = generate_sql(question)

                st.subheader("🧾 Generated SQL")
                st.code(sql_query, language="sql")

                # Safety check
                if any(word in sql_query.lower() for word in ["drop", "delete", "update", "insert"]):
                    st.error("❌ Unsafe query blocked!")
                else:
                    conn = get_connection()
                    cursor = conn.cursor()

                    try:
                        cursor.execute(sql_query)
                        results = cursor.fetchall()

                        st.subheader("📊 Results")

                        if results:
                            st.dataframe(results)
                        else:
                            st.info("No results found.")

                    except Exception as e:
                        st.error(f"Query Error: {e}")

            except Exception as e:
                st.error(f"Error: {e}")