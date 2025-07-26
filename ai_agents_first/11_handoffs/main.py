from dotenv import  load_dotenv
from agents import Agent , Runner ,AsyncOpenAI , OpenAIChatCompletionsModel , handoffs
import os 
from agents.run import RunConfig

load_dotenv()


google_api_key = os.getenv("GEMNIN_API_KEY") 

client = AsyncOpenAI(
    api_key= google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"   
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= client
)
config = RunConfig(
        model=model,
        model_provider= client,
        tracing_disabled=True
)

python_Agent = Agent(
    name = "Python_Agent",
    instructions= "You are an intelligent Python assistant. Help users understand and interact with Python-based tools or APIs, and explain code or results clearly.",
    model = model
)
Nextjs_Agent = Agent(
    name = "Nextjs_Agent",
    instructions= "You are a helpful assistant for a Next.js website. Guide users, answer their questions clearly, and explain how to use the site effectively.",
    model = model
)

agent = Agent(
    name = "Triage_Agent",
    instructions= "You are a smart triage agent. Analyze user input, identify the issue type and urgency, and route it to the correct category or team with a clear summary.",
    model = model,
    handoffs= [python_Agent,Nextjs_Agent]

)

prompt = input("What can I help with?\n ")

def main():

    result = Runner.run_sync(agent , prompt, run_config=config)
    print(result.final_output)

if __name__ == "__main__" :
    main()    

