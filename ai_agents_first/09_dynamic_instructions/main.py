from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunContextWrapper, set_tracing_disabled
from dotenv import load_dotenv
import datetime
import os

# 🔹 Load .env file
load_dotenv()

# 🔹 Disable tracing to avoid OpenAI key warning
set_tracing_disabled(disabled=True)

# 🔹 Gemini API key
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

# 🔹 External Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url=base_url
)

# 🔹 Model setup with Gemini
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# -------------------------
# Dynamic Instructions Class
# -------------------------
class SmartInstructions:
    def __init__(self):
        self.interaction_count = 0

    def __call__(self, context: RunContextWrapper, agent: Agent) -> str:
        self.interaction_count += 1
        message_count = len(getattr(context, "messages", []))
        user_name = getattr(context.context, "name", "user")

        # Time-based greeting
        hour = datetime.datetime.now().hour
        if 6 <= hour < 12:
            time_greeting = "Good morning"
        elif 12 <= hour < 17:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"

        # 🧠 Dynamic behavior
        if self.interaction_count == 1:
            return f"{time_greeting}, {user_name}! I am {agent.name}. This is our first chat – I’ll be welcoming and friendly."
        elif message_count < 3:
            return f"{time_greeting}, {user_name}! You are talking to {agent.name}. I’ll explain things in detail."
        else:
            return f"{time_greeting}, {user_name}! We've interacted {self.interaction_count} times. I’ll be concise and efficient now."

# -------------------------
# Create Agent with Gemini model
# -------------------------
agent = Agent(
    name="Smart Assistant",
    instructions=SmartInstructions(),
    model=model   # ✅ Gemini model attach kiya
)

# -------------------------
# Test runs
# -------------------------
if __name__ == "__main__":
    result1 = Runner.run_sync(agent, "Hello!")
    print("First run:", result1.final_output)

    result2 = Runner.run_sync(agent, "Can you explain Python functions?")
    print("Second run:", result2.final_output)

    result3 = Runner.run_sync(agent, "Thanks, and what about classes?")
    print("Third run:", result3.final_output)
