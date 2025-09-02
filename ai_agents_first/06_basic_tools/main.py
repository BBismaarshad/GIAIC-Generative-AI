import os 
from agents import Agent , Runner , AsyncOpenAI , OpenAIChatCompletionsModel , function_tool , set_tracing_disabled
from dotenv import load_dotenv 

load_dotenv()
set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= BASE_URL
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client=external_client
)

@function_tool
def multiply(a: int , b: int) -> int:
    return a * b

@function_tool
def sum(a:int, b:int)-> int:
    return a+b 


agent = Agent(
    name = "Assistant",
    instructions= ("You are a helpful assistant."
    "Alway use tools for math questions. Always follaw DMAS rule."
    ),
    model = model ,
    tools = [multiply , sum ]
)

prompt = "what is 19 + 23 * 2 ?"
result = Runner.run_sync(agent, prompt)
print(result.final_output)