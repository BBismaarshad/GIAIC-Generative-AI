from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import requests

load_dotenv()

set_tracing_disabled(disabled=True)

google_api_key = os.getenv("GEMINI_API_KEY") 


client = AsyncOpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Setup model with correct name
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Define a tool function to fetch weather
@function_tool
def calling_api_weather(city: str) -> str:
    """
    Get the weather for a given city using WeatherAPI.
    """
    try:
        response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key=8e3aca2b91dc4342a1162608252604&q={city}"
        )
        data = response.json()

        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]

        return f"The current weather in {city} is {temperature}°C with {condition}."

    except Exception as e:
        return f"Could not fetch weather data due to: {e}"

# Create agent
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model=model,
    tools=[calling_api_weather]
)

# Main function to run the agent
def main():
    prompt = input("What can I help with?\n> ")
    result = Runner.run_sync(agent, prompt)
    print(result.final_output)


if __name__ == "__main__":
    main()
