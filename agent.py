from tools.clinical_trials_api import ClinicalTrialsAPI
from tools.drug_retrieval import retriever
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

# Your other tools (e.g., Chroma RAG)
tools = [
    rag_tool,               # your Chroma retriever wrapped as a Tool
    trial_lookup_tool(),    # this tool!
    DuckDuckGoSearchRun(name="WebSearch")
]

llm = ChatOpenAI(model_name="gpt-4", temperature=0)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
