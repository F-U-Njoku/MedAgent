import os
from pyexpat.errors import messages
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

import torch
torch.classes.__path__ = []


import sys
import pysqlite3

sys.modules['sqlite3'] = pysqlite3
from langchain_core.messages import AIMessage

import streamlit as st
from agent import medagent

def content_to_text(content) -> str:
    # content can be a string OR a list of blocks like [{"type":"text","text":"..."}]
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text" and "text" in block:
                    parts.append(block["text"])
                elif "content" in block:
                    parts.append(str(block["content"]))
                else:
                    # fallback: keep something readable
                    parts.append(str(block))
            else:
                parts.append(str(block))
        return "\n".join(parts).strip()
    return str(content)


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
                result = medagent.invoke({"messages": [{"role": "user", "content": query}]})
                messages = result.get("messages", result)  # sometimes it's already a list
                
                final_text = None
                if isinstance(messages, list):
                    for m in reversed(messages):
                        if isinstance(m, AIMessage):
                            final_text = content_to_text(m.content)  # <-- normalize here
                            break
                        if isinstance(m, dict) and m.get("role") in ("assistant", "ai"):
                            final_text = content_to_text(m.get("content"))
                            break
                if not final_text:
                    final_text = str(result)

                st.markdown("### 🧠 Answer")
                st.markdown(final_text)
            except Exception as e:
                st.error("Something went wrong. Please try again.")
                st.exception(e)

    if st.checkbox("Show agent debug trace"):
        with st.expander("Agent Debug Logs"):
            st.code(result)  

if __name__ == "__main__":
    main()