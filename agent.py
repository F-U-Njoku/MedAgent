import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentType
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

tools = [drug_tool, search_trials, web_tool]

prompt = PromptTemplate(
        input_variables=["input", "agent_scratchpad"],
        template="""You are a helpful medical information agent. 
        Use the available tools to answer medical questions accurately.
        
        You have access to these tools:
        {tools}
        
        Question: {input}
        {agent_scratchpad}"""
    )

# 🚀 Initialize the agent
medagent = create_react_agent(
    tools=tools,
    llm=llm
)
