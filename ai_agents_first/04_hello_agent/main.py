from dotenv import load_dotenv
import os
from agents import Agent , Runner, AsyncOpenAI , OpenAIChatCompletionsModel
from agents.run import RunConfig
 
load_dotenv()

client = AsyncOpenAI(
   api_key= os.getenv("GEMINI_API_KEY"),
   base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client

)

config = RunConfig(
    model = model,
    model_provider= client,
    tracing_disabled= True
)
agent = Agent(
    name = "Assistant",
    instructions= "Your are a Helpfull Assistant.",
    model = model
)
def main():
    
    prompt = input("Hello Agent ")
    result = Runner.run_sync(agent, prompt, run_config=config)

    print(result.final_output)

if __name__ == "__main__":
    main()

