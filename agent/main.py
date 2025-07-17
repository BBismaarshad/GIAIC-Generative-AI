from openai import AsyncOpenAI
from agents import Agent , OpenAIChatCompletionsModel , Runner , set_tracing_disabled
import asyncio

gemini_api_key="AIzaSyB9uDK8do_YnDSr1VkCav1STGZmroQeJqs "
client = AsyncOpenAI(
    api_key=gemini_api_key,
     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

set_tracing_disabled(disablad=True)

async def main():
    agent =Agent(
        name = "Assistant",
        instruction = "You only respond in haikus",
        model = "gemini-2.0-flash",
        openai_client=client
    )
    
    result = await Runner.run(agent, "Recursion kya hoti hai?")

if __name__ == "__main__":
    asyncio.run(main())    
