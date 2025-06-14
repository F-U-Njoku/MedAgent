import streamlit as st
from agent import medagent

# 🧪 App Config
st.set_page_config(page_title="MedAgent 💊", layout="centered")
st.title("💊 MedAgent: Your AI Drug Assistant")

# 🧠 Input Prompt
query = st.text_input("Ask a drug-related question (e.g., 'What are the side effects of metformin?')")

# 🚀 Process Query
if query:
    with st.spinner("Thinking..."):
        try:
            result = medagent.run(query)
            st.markdown("### 🧠 Answer")
            st.markdown(result)
        except Exception as e:
            st.error("Something went wrong. Please try again.")
            st.exception(e)

if st.checkbox("Show agent debug trace"):
    with st.expander("Agent Debug Logs"):
        st.code(result)  