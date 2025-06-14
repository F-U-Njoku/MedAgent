import os
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

import streamlit as st
from agent import agent_executor

def main():
    # 🧪 App Config
    st.set_page_config(page_title="MedAgent 💊", layout="centered")
    st.title("💊 MedAgent: Your AI Drug Assistant")

    # 🧠 Input Prompt
    query = st.text_input("Ask a drug-related question (e.g., 'What are the side effects of metformin?')")

    # 🚀 Process Query
    if query:
        with st.spinner("Thinking..."):
            try:
                result = agent_executor.invoke({"input": query})
                st.markdown("### 🧠 Answer")
                st.markdown(result["output"])
            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.exception(e)

    if st.checkbox("Show agent debug trace"):
        with st.expander("Agent Debug Logs"):
            st.code(result)  

if __name__ == "__main__":
    main()