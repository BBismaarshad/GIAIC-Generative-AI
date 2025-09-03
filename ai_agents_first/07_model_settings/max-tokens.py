from agents import Agent, Runner, AsyncOpenAI, ModelSettings, set_tracing_disabled, OpenAIChatCompletionsModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Disable tracing to avoid warning about OPENAI_API_KEY
set_tracing_disabled(disabled=True)

# Gemini setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# External client for Gemini
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# Model configuration
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Creative agent
creative = Agent(
    name="Creative Writer",
    instructions="Write vivid, imaginative stories.",
    model=model,
    model_settings=ModelSettings(temperature=0.9, max_tokens=350)  # more creative
)

# Run the agent
result = Runner.run_sync(creative, "Hello Gemini, write a short story about a robot.")
print(result.final_output)
