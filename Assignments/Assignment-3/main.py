# library_assistant.py

from dotenv import load_dotenv
import os
from pydantic import BaseModel
from agents import Agent, Runner, OpenAIChatCompletionsModel, dynamic_instruction
from agents.tool import function_tool
from agents.guardrail import input_guardrail, GuardrailFunctionOutput
from agents.run import RunConfig
import asyncio

# --------------------------
# 1. Load API Key
# --------------------------
load_dotenv()
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------
# 2. Book Database
# --------------------------
books_db = {
    "Python 101": 3,
    "AI Basics": 0,
    "Data Science Handbook": 5
}

# --------------------------
# 3. User Context Model
# --------------------------
class UserContext(BaseModel):
    name: str
    member_id: str

# --------------------------
# 4. Guardrail Agent (Only Library Questions Allowed)
# --------------------------
guardrail_agent = Agent(
    name="LibraryGuard",
    model=OpenAIChatCompletionsModel(
        api_key=GEMINI_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ),
    instructions="""
    You are a guardrail for a library assistant.
    If the query is NOT related to books, library timings, or availability,
    respond with: "REJECT".
    Otherwise, respond with: "ALLOW".
    """
)

@input_guardrail
async def library_input_guardrail(ctx, query: str) -> GuardrailFunctionOutput:
    result = await guardrail_agent.run(query=query)
    if "REJECT" in result.output_text:
        return GuardrailFunctionOutput(
            is_tripwire_triggered=True,
            message="❌ Sorry, I can only answer library-related questions."
        )
    return GuardrailFunctionOutput(is_tripwire_triggered=False)

# --------------------------
# 5. Member Validation
# --------------------------
def is_valid_member(user: UserContext):
    return user.member_id.startswith("LIB")

# --------------------------
# 6. Search Book Tool
# --------------------------
@function_tool
def search_book(book_name: str) -> str:
    """Search if a book exists in the library database."""
    if book_name in books_db:
        return f"✅ The book '{book_name}' is available in our library."
    return f"❌ The book '{book_name}' is not found in our library."

# --------------------------
# 7. Check Availability Tool (Members only)
# --------------------------
@function_tool
def check_availability(user: UserContext, book_name: str) -> str:
    """Check how many copies of a book are available. Only for registered members."""
    if not is_valid_member(user):
        return "🚫 You must be a registered library member to check availability."
    if book_name in books_db:
        return f"📚 We have {books_db[book_name]} copies of '{book_name}' available."
    return f"❌ The book '{book_name}' is not in our library."

# --------------------------
# 8. Main Library Agent
# --------------------------
library_agent = Agent(
    name="LibraryAssistant",
    model=OpenAIChatCompletionsModel(
        api_key=GEMINI_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    ),
    instructions="You are a helpful library assistant. Answer only library-related questions.",
    tools=[search_book, check_availability],
    input_guardrail=library_input_guardrail,
    dynamic_instructions=[
        dynamic_instruction(lambda ctx: f"Hello {ctx.user.name}, welcome to our library!")
    ]
)

# --------------------------
# 9. Testing the Agent
# --------------------------
async def main():
    user = UserContext(name="Bisma", member_id="LIB123")

    test_queries = [
        "Search book Python 101",
        "Check availability for AI Basics",
        "What time does the library open?",
        "Tell me a joke"  # This should be rejected
    ]

    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        result = await Runner.run(
            agent=library_agent,
            user=user,
            input=query,
            run_config=RunConfig(stream=False)
        )
        print("💬 Response:", result.output_text)

if __name__ == "__main__":
    asyncio.run(main())
