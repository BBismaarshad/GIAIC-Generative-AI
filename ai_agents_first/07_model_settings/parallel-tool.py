from agents import Agent, Runner, ModelSettings, set_tracing_disabled, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Disable tracing
set_tracing_disabled(disabled=True)

# Gemini API setup
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Tools
@function_tool
def weather_tool(query: str) -> str:
    """Get weather information for a given location"""
    return f"Weather info for: {query}"

@function_tool
def calculator(expression: str) -> str:
    """Evaluate a math expression"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"

@function_tool 
def translator(text: str, lang: str = "ur") -> str:
    """Translate text into a given language (default Urdu)"""
    return f"Translated '{text}' to {lang}"   

# Agent
multi = Agent(
    name="Multi-tasker",
    instructions="You are a helpful multi-task agent. Use tools when needed.",
    model=model,
    tools=[weather_tool, calculator, translator],
    model_settings=ModelSettings(
        tool_choice="auto",
        parallel_tool_calls=False  
    )
)

# Run Agent with a sample query
result = Runner.run_sync(
    multi,
    "Translate 'Hello, how are you?' into Urdu and then calculate 5*10"
)

print(result.final_output)
