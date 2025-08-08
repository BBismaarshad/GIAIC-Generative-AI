#GLOBAL-level configuration 
from agents import Agent , Runner , AsyncOpenAI ,  set_tracing_disabled , set_default_openai_api

gemini_api_key = ""

set_tracing_disabled(True)

set_default_openai_api("chat_completions")

external_client = AsyncOpenAI(
    api_key= "gemini_api_key",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

agent: Agent = Agent(
    name="Assistant", 
    instructions="You are a helpful assistant", 
    model="gemini-2.0-flash"
)


result = Runner.run_sync(agent, "Hello")

print(result.final_output)