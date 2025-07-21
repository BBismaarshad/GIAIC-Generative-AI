from dotenv import load_dotenv
from agents import Agent , Runner , OpenAIChatCompletionsModel , AsyncOpenAI
from agents.run import RunConfig
import os

load_dotenv()

client = AsyncOpenAI(
    api_key= os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
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
    name = "Product Suggester",
    instructions= """You are a helpful Smart Store Assistant.

Your job is to suggest a product based on the user's need, symptom, or problem. 
Then explain why you are suggesting that product.

Follow these rules:
1. Understand the user's problem or need.
2. Suggest one product that is suitable.
3. Give a short and clear explanation of why this product is helpful.""",
    model = model
)

prompt = input("Hey! Need a product? I’m here to help! :\n")
def main():
     result = Runner.run_sync(agent ,prompt, run_config=config)
     print(result.final_output)
     
if __name__ == "__main__":
     main()     

