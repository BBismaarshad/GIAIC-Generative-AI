from agents import Agent , Runner , AsyncOpenAI , ModelSettings ,OpenAIChatCompletionsModel , set_tracing_disabled , function_tool
import os 
from dotenv import load_dotenv

load_dotenv()

set_tracing_disabled(disabled=True)

gemini_api_key = os.getenv("GEMINI_API_KEY")
Base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=Base_url
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)


@function_tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers exactly."""
    return a * b

math_agent = Agent(
    name="Math Teacher",
    instructions="You are a math teacher. Always solve step by step and explain clearly.",
    tools=[multiply],
    model=model,   
    model_settings=ModelSettings(
        temperature=0.2,
        max_tokens=200,
        tool_choice="required"
    )
)


result = Runner.run_sync(math_agent, "Solve 12 * 7 step by step")

print("Agent Output:\n", result.final_output)
