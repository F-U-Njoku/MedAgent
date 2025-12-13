import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chat_models import init_chat_model

from tools.drug_retrieval import retrieve_drug_info
from tools.clinical_trial_tool import clinical_trials_tool

load_dotenv(dotenv_path=".env", override=True)

# 🔐 Ensure key is loaded
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not set. Check your .env file.")

# ✅ GPT-4 model
llm = init_chat_model(os.getenv("MODEL_NAME"), 
                      model_provider="google_genai", 
                      api_key=os.getenv("GEMINI_API_KEY"))

# Tool 1: Drug info from local RAG index
@tool("DrugInfo")
def drug_tool(q: str) -> str:
    """Extract detailed drug information (uses, side effects, precautions) from local MedlinePlus data.
    Input: string drug name.
    """
    return "\n\n".join(doc.page_content for doc in retrieve_drug_info(q))
# Tool 2: Clinical trials search

# Tool 3: Web search fallback
web_search_tool = DuckDuckGoSearchRun(name="WebSearch")

tools = [drug_tool, clinical_trials_tool, web_search_tool]

agent_prompt = '''You are a helpful medical information agent. 
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

prompt = PromptTemplate.from_template(agent_prompt)


# 🚀 Initialize the agent
medagent = create_agent(
    tools=tools,
    model=llm,
    system_prompt=agent_prompt
)