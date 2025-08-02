
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import requests

# Load environment variables
load_dotenv()
set_tracing_disabled(disabled=True)

# Load Gemini API key
google_api_key = os.getenv("GEMINI_API_KEY")

# Create Gemini client and model
client = AsyncOpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

#tools

@function_tool
def capital_api(country: str) -> str:
    """Get the capital of a country using REST Countries API."""
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        data = response.json()
        if isinstance(data, list) and "capital" in data[0]:
            return data[0]["capital"][0]
        else:
            return "Capital not found."
    except Exception as e:
        return f"Error fetching capital: {e}"

@function_tool
def language_api(country: str) -> str:
    """Get the language(s) of a country using REST Countries API."""
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and "languages" in data[0]:
            return ", ".join(data[0]["languages"].values())
        return "Languages not found."
    except Exception as e:
        return f"Error fetching language: {e}"

@function_tool
def population_api(country: str) -> str:
    """Get the population of a country using REST Countries API."""
    try:
        response = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and "population" in data[0]:
            return f"{data[0]['population']:,} people"
        return "Population data not found."
    except Exception as e:
        return f"Error fetching population: {e}"

# Capital Agent
capital_agent = Agent(
    name="CapitalAgent",
    instructions="You provide the capital of a country.",
    model=model,
    tools=[capital_api]
)

# Language Agent
language_agent = Agent(
    name="LanguageAgent",
    instructions="You provide the official languages of a country.",
    model=model,
    tools=[language_api]
)

# Population Agent
population_agent = Agent(
    name="PopulationAgent",
    instructions="You provide the population of a country.",
    model=model,
    tools=[population_api]
)

# Convert tool agents into tools
capital_tool = capital_agent.as_tool(
    tool_name="capital_tool",
    tool_description="Get the capital city of a country"
)

language_tool = language_agent.as_tool(
    tool_name="language_tool",
    tool_description="Get the official languages of a country"
)

population_tool = population_agent.as_tool(
    tool_name="population_tool",
    tool_description="Get the population of a country"
)

# Orchestrator agent
orchestrator = Agent(
    name="CountryInfoOrchestrator",
    instructions="""
You are a helpful assistant that provides full country info including:
1. Capital
2. Official language(s)
3. Population

Use the provided tools to gather this information.
""",
    model=model,
    tools=[capital_tool, language_tool, population_tool]
)

def main():
    prompt = input("Enter country name:\n> ")
    result = Runner.run_sync(orchestrator, prompt)
    print("\n--- Country Information ---")
    print(result.final_output)

if __name__ == "__main__":
    main()
