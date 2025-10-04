from agents import Agent , Runner, OpenAIChatCompletionsModel , set_tracing_disabled, enable_verbose_stdout_logging
from dotenv import load_dotenv
from  openai import AsyncOpenAI
import os

load_dotenv()

enable_verbose_stdout_logging()

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
   api_key= os.getenv("GEMINI_API_KEY"),
   base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client

)

web_search_agent = Agent(
    name = "Websearchaget" ,
    instructions= "you perform a web seach and return useful content for the give topic.",
    model = model 
)

#as tool web search 

web_search_agent_as_tool = web_search_agent.as_tool(
    tool_name = "web_search_tool",
    tool_description="you perform a web seach and return useful content for the give topic."
) 
# agent data analysis
data_analysis_agent = Agent (
    name = "DataAnalysisAgent",
    instructions=" You analyze topic-related informtion and extract key inside ",
    model = model 
)
# as tool data analysis

data_analysis_agent_as_tool = data_analysis_agent.as_tool(
    tool_name = "data_anaylysis_tool",
    tool_description = " You analyze topic-related informtion and extract key inside ",   
)

# writer agent
writer_agent = Agent (
    name = "writerAgent",
    instructions = "You write a formal , structure report base on prompt ",
    model = model 
)
# writer agent as tool
writer_agent_as_tool = writer_agent.as_tool(
    tool_name = "writer_agebnt_tool",
    tool_description = "You write a formal , structure report base on prompt ",
)

# Orchestration agent 
main_agent = Agent(
    name = "Orchestration main agent",
    instructions= """
You are an intelligent orchestrator agent .
1. use 'websearchAgent' to gather information about topic user requested.
2. send that information to  'DataAnalysisAgent' to generate insights.
3. pass Those insights to 'writerAgent' to Generate final report.
""",
    model = model ,
    tools= [web_search_agent_as_tool , data_analysis_agent_as_tool , writer_agent_as_tool]
)

result = Runner.run_sync( main_agent, input = "What are the things an AI agent can do?")

print(result.final_output)