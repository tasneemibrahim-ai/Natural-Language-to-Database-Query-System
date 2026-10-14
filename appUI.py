import streamlit as st
from main import query_to_sql
from db_setup import setup_database, get_schema

st.set_page_config(page_title="Text-to-SQL System", layout="wide", page_icon="🧠")

st.title("🧠 Natural Language to Database Query System")
st.caption("Ask questions about the database in plain English · Powered by Groq LLaMA-3 + LangChain")

# Ensure DB is ready
setup_database()

with st.sidebar:
    st.header("📋 Database Schema")
    try:
        st.code(get_schema(), language="sql")
    except Exception as e:
        st.warning(f"Could not load schema: {e}")

question = st.text_input("Enter your question:", placeholder="e.g. Show all users from New York")

if st.button("🚀 Generate & Execute", type="primary"):
    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Generating SQL & Executing..."):
            res = query_to_sql(question.strip())
            
            if res["sql"]:
                st.subheader("🧾 Generated SQL")
                st.code(res["sql"], language="sql")
                
            if res["error"]:
                st.error(f"❌ {res['error']}")
            elif res["dataframe"] is not None:
                st.subheader(f"📊 Results ({len(res['dataframe'])} row(s))")
                st.dataframe(res["dataframe"], use_container_width=True)
                st.download_button("⬇ Download CSV", res["dataframe"].to_csv(index=False), "query_results.csv", "text/csv")