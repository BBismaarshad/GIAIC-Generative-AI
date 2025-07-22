from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import os

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

Mood_Checker = Agent(
    name="MoodChecker",
    instructions="""
You are a helpful mood detection assistant.
Your job is to read the user's message and respond with their mood as one word.
Possible moods: happy, sad, angry, excited, stressed, relaxed, bored.

Just reply with the mood only.
Example:
User: I'm feeling down today
You: sad
""",
    model=model
)

Activity_Suggester = Agent(
    name="ActivitySuggester",
    instructions="""
You are a helpful assistant that suggests a positive activity based on a person's mood.
Your job is to suggest appropriate activities based on their current mood.
For positive moods (happy, excited, relaxed), suggest activities to enhance or maintain their good mood.
For negative moods (sad, angry, stressed, bored), suggest activities to improve their mood.

""",
    model=model
)

def main():
    prompt = input("Hey! How are you feeling today?\n>")
    
    # First detect the mood
    mood_result = Runner.run_sync(Mood_Checker, prompt, run_config=config)
    mood = mood_result.final_output.strip().lower()
    print(f"\nDetected mood: {mood}\n")
    
    # Then get activity suggestion based on the mood
    activity_result = Runner.run_sync(Activity_Suggester, mood, run_config=config)
    print(f"\nSuggested activity: {activity_result.final_output}")

if __name__ == "__main__":
    main()