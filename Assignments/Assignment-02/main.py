import asyncio
from dotenv import load_dotenv
from agents import Agent , Runner , function_tool , OpenAIChatCompletionsModel , AsyncOpenAI ,RunContextWrapper
import os 
from agents.run import RunConfig
from pydantic import BaseModel

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
class Account(BaseModel):
    name : str
    pin: int

def check_user(ctx:RunContextWrapper[Account],agent:Agent) -> bool:
    if ctx.context.name == "Bisma" and ctx.context.pin == 5678:
        return True
    else:
        return False



@function_tool (is_enabled = check_user)
def check_balance(account_number :str ) -> str:
    return f"The balance of account is $2000000"


bank_agent = Agent(
    name = "Bank_Agent",
    instructions= "You are  a bank  agent. You help customers with theri questions Your can use the tools to get the .",
    tools=[check_balance]

)

user_context = Account(name="Bisma", pin= 5678)
propmt =input( "Hello ma Bankig Agent! What can a help you:\n ")

def main():
    result = Runner.run_sync(bank_agent , propmt , context=user_context, run_config=config )
    print(result.final_output)

if __name__ == "__main__" :
    main()      
    


