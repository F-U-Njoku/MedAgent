## 💊 MedAgent: A GenAI Assistant for Drug Insights

**MedAgent** is an agent-powered AI assistant that answers drug-related questions using Retrieval-Augmented Generation (RAG), live clinical trial data, and web search — tailored for healthcare professionals, researchers, and medical learners.

This project showcases:

* LangChain ReAct agent orchestration
* Chroma vector store indexing
* Streamlit UI deployment
* ClinicalTrials.gov API integration
* DuckDuckGo web fallback

---

## ✨ Features

* 🧠 **LLM-Powered QA**: Uses Google Gemini (via Google GenAI API) to reason and answer complex drug-related questions.
* 🔍 **RAG from MedlinePlus**: Retrieves indexed drug usage, side effects, and precautions.
* 🧪 **Live Clinical Trials**: Queries real-time data from ClinicalTrials.gov via API v2.
* 🌐 **Web Fallback**: DuckDuckGo integration to answer open-ended or time-sensitive questions.
* 📆 **Streamlit UI**: Simple, user-friendly web interface.
* 🧰 **Agentic Reasoning**: Built with `create_react_agent` using LangChain’s ReAct pattern.

---

## 🧱 Tech Stack

| Layer        | Tech                                                   |
| ------------ | ------------------------------------------------------ |
| 💬 LLM       | `Google Gemini`                                        |
| 📚 RAG       | `LangChain`, `HuggingFaceEmbeddings`, `Chroma` |
| 🔎 Tools     | `DuckDuckGoSearch`, `ClinicalTrials.gov API`           |
| 🌐 UI        | `Streamlit`                                            |
| ⚡ Env Mgmt  | `uv`                                                   |
| 📦 Packaging | `pyproject.toml`, `uv.lock`                            |
| 📀 Storage   | Local CSV + vectorstore                                |

---

## 📁 File Structure

```
medagent/
├── chroma_db/              # Vector store (if Chroma)
├── data/
│   └── medlineplus_drugs.csv
├── tools/
│   ├── clinical_trials_api.py      # API wrapper for ClinicalTrials.gov
│   ├── clinical_trial_tool.py      # LangChain Tool wrapper
│   └── drug_retrieval.py           # Vector search tool (Chroma/FAISS)
├── utils/
│   ├── ingest_embed.py             # Index CSV data to vectorstore
│   └── scrape.py                   # Scrapes MedlinePlus drug info
├── app.py                 # Streamlit frontend
├── agent.py               # ReAct agent setup & execution
├── .env                   # Stores GEMINI_API_KEY
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## 🛠️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourname/medagent.git
   cd medagent
   ```

2. **Set up environment with uv**

   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Sync dependencies
   uv sync
   ```

3. **Set your API key**
   Create a `.env` file:

   ```
   GEMINI_API_KEY=your-google-genai-key
   MODEL_NAME=gemini-pro
   ```

4. **Scrape and embed drug data**

   ```bash
   uv run python utils/scrape.py
   uv run python utils/ingest_embed.py
   ```

5. **Run Streamlit**

   ```bash
   uv run -- streamlit run app.py
   ```

---

## 🧪 Example Queries

* “What are the side effects of metformin?”
* “Are there ongoing clinical trials for GLP-1 receptor agonists?”
* “Latest FDA warning about Ozempic”
* “Compare ibuprofen and acetaminophen on safety”

---

## 🧠 Agent Flow (ReAct Pattern)

```plaintext
Question → Thought → Action → Observation → Thought → ... → Final Answer
```

MedAgent dynamically chooses tools: local vectorstore, clinical trials API, or DuckDuckGo — depending on the query type.

---

## 🔐 Notes

* Chroma requires SQLite ≥ 3.35, so I patched it using `pysqlite3-binary` for Streamlit compatibility.
* Streamlit file watcher disabled to avoid `torch.classes` runtime error.

---

## 💡 Future Ideas

* Add LangGraph-style tool-switching with memory
* Enable live filtering on clinical trial results
* Add caching + logging for auditability
* Deploy via Docker or Hugging Face Spaces

---

## 📄 License

MIT — free for personal and commercial use.

---

## 🙌 Acknowledgments

* [LangChain](https://www.langchain.com/)
* [MedlinePlus](https://medlineplus.gov/)
* [ClinicalTrials.gov](https://clinicaltrials.gov/)
