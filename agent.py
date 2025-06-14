import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
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

# Tool 1: Drug info from local RAG index
drug_tool = Tool(
    name="DrugInfoRetriever",
    func=lambda q: "\n\n".join(doc.page_content for doc in retrieve_drug_info(q)),
    description=(
        "Extract detailed drug information (uses, side effects, precautions) "
        "from local MedlinePlus data. Input: string drug name."
    ),
)

# Tool 2: ClinicalTrials.gov live lookup
clinical_trials_tool = get_clinical_trials_tool()

# Tool 3: Web search fallback
web_search_tool = DuckDuckGoSearchRun(name="WebSearch")

tools = [drug_tool, clinical_trials_tool, web_search_tool]

template = '''You are a helpful medical information agent. 
        Use the available tools to answer medical questions accurately.
        You have access to these tools:
        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Action: the action to take, should be one of [{tool_names}]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can repeat 5 times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question.
        If you don't have a satisfactory answer, you can creatively say you don't know.

        Begin!

        Question: {input}
        Thought:{agent_scratchpad}'''

prompt = PromptTemplate.from_template(template)


# 🚀 Initialize the agent
medagent = create_react_agent(
    tools=tools,
    llm=llm,
    prompt=prompt
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=medagent,
    tools=tools,
    verbose=True
)