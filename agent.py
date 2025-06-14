import pysqlite3
import sys
sys.modules['sqlite3'] = pysqlite3

import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_openai import ChatOpenAI

from tools.drug_retrieval import retrieve_drug_info
from tools.clinical_trial_tool import get_clinical_trials_tool

load_dotenv()

# 🔐 Ensure key is loaded
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not set. Check your .env file.")

# ✅ GPT-4 model
llm = ChatOpenAI(model_name="gpt-4", temperature=0)

# 🧠 Tool 1: Drug info from Chroma
drug_tool = Tool(
    name="DrugInfoRetriever",
    func=lambda q: "\n\n".join([doc.page_content for doc in retrieve_drug_info(q)]),
    description="Use this tool to retrieve information about drug usage, side effects, and precautions."
)

# 🧠 Tool 2: ClinicalTrials.gov search
search_trials = get_clinical_trials_tool()

# 🧠 Tool 3: DuckDuckGo web search
web_tool = DuckDuckGoSearchRun(name="WebSearch")

# 🚀 Initialize the agent
medagent = initialize_agent(
    tools=[drug_tool, search_trials, web_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)