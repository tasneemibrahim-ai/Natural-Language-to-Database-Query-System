import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from db_setup import setup_database, get_schema
from main import query_to_sql

st.set_page_config(page_title="Text-to-SQL", page_icon="🗄️", layout="wide")
st.title("🗄️ Text-to-SQL with Llama3 (Groq)")
st.caption("Natural language → SQL → Results · Powered by Groq + LangChain")

# Validate Groq key on startup
if not os.getenv("GROQ_API_KEY"):
    st.error("❌ GROQ_API_KEY not found. Add it to your .env file and restart the app.")
    st.code("GROQ_API_KEY=gsk_your-key-here", language="bash")
    st.stop()

# Init DB on startup
with st.spinner("Initializing database..."):
    try:
        setup_database()
    except Exception as e:
        st.error(f"Database init failed: {e}")
        st.stop()

# Sidebar: schema + examples
with st.sidebar:
    st.header("📋 Database Schema")
    try:
        st.code(get_schema(), language="sql")
    except Exception as e:
        st.warning(f"Could not load schema: {e}")

    st.divider()
    st.subheader("💡 Example Queries")
    examples = [
        "Show all users from New York",
        "What are the top 3 most expensive products?",
        "How many orders has each user placed?",
        "List all delivered orders with user names and product names",
        "What is the total revenue per product category?",
    ]
    for ex in examples:
        if st.button(ex, use_container_width=True):
            st.session_state["query_input"] = ex

    st.divider()
    st.subheader("🤖 Model")
    st.markdown("**Groq** · `llama3-8b-8192`")

# Query input
query = st.text_area(
    "Enter your question:",
    value=st.session_state.get("query_input", ""),
    height=80,
    placeholder="e.g. Show me all users who placed more than 1 order",
    key="query_input",
)

col1, col2 = st.columns([1, 5])
with col1:
    run = st.button("▶ Run Query", type="primary", use_container_width=True)
with col2:
    if st.button("🧹 Clear", use_container_width=True):
        st.session_state["query_input"] = ""
        st.rerun()

if run and query.strip():
    with st.spinner("Generating SQL and executing..."):
        result = query_to_sql(query.strip())

    st.subheader("Generated SQL")
    if result["sql"]:
        st.code(result["sql"], language="sql")
    else:
        st.warning("No SQL was generated.")

    if result["error"]:
        st.error(f"❌ {result['error']}")
    elif result["dataframe"] is not None:
        df = result["dataframe"]
        st.subheader(f"Query Results — {len(df)} row(s)")
        if df.empty:
            st.info("Query returned no results.")
        else:
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇ Download CSV", df.to_csv(index=False), "results.csv", "text/csv")
elif run:
    st.warning("Please enter a question first.")
