from agents import Agent, Runner, ModelSettings, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# External client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Agent setup
math_tutor = Agent(
    name="Math Tutor",
    instructions="Precise math. Show steps.",
    model=model,
    model_settings=ModelSettings(temperature=0.1, max_tokens=400)
)

# Run synchronously
result = Runner.run_sync(math_tutor, "Solve : 2*3+89 ")
print(result.final_output)
