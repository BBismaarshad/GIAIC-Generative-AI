from agents import Agent, Runner , ModelSettings , function_tool, AsyncOpenAI , OpenAIChatCompletionsModel , set_tracing_disabled ,function_tool
from dotenv import load_dotenv
import os

load_dotenv()
set_tracing_disabled(disabled=True)
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url="https://generativelanguage.googleapis.com/v1beta/openai/"


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url= base_url
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.5-flash",
    openai_client= external_client
)

#Tool Choice

@function_tool
def calculate_area(
    lenght :float , width : float) -> float:
    return lenght * width

tool_user = Agent(
    name = "Tool User",
    instructions="Always use tool available",
    model =model ,
    tools= [calculate_area],
    model_settings= ModelSettings(tool_choice="required")
)

result = Runner.run_sync(tool_user , "Area of 5 by 3?")
print(result.final_output)


