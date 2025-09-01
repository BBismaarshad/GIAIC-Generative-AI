from dotenv import load_dotenv
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl

# 🔑 Load environment variables
load_dotenv()

# ✅ Gemini API client setup
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# ✅ Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# ✅ Run configuration
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# ✅ Agent setup
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model
)

# 🌟 Chat start event
@cl.no_chat_start
async def handle_start():
    cl.user_session.set("history", [])  # Session history initialize
    await cl.Message(content="Hello! I am your assistant.").send()

# 🌟 On user message
@cl.on_message
async def handle_message(message: cl.Message):
    # 1️⃣ Get history from session
    history = cl.user_session.get("history") or []

    # 2️⃣ Append user message to history
    history.append({"role": "user", "content": message.content})

    # 3️⃣ Run agent with updated history
    result = await Runner.run(
        agent,
        input=history,
        run_config=config
    )

    # 4️⃣ Append agent response to history
    history.append({"role": "assistant", "content": result.final_output})

    # 5️⃣ Save updated history back to session
    cl.user_session.set("history", history)

    # 6️⃣ Send response to user
    await cl.Message(content=result.final_output).send()
