from dotenv import load_dotenv
from agents import Agent, Runner
import os


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

gemini_agent = Agent(
    name = "Assistant",
    instructions = f"You are a Helpfull Assistant.{api_key}" 
)

def main():
    prompt = input("Ask any Questions?")
    result = Runner.run_sync(gemini_agent,prompt)
    print(result.final_output)


