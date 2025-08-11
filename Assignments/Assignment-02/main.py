from dotenv import load_dotenv
import os
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    function_tool,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    RunContextWrapper
)
from agents.run import RunConfig

# Load environment variables
load_dotenv()

# API Key
google_api_key = os.getenv("GEMINI_API_KEY")

# Create async client for Gemini
client = AsyncOpenAI(
    api_key=google_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Model setup
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)

# Run configuration
config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# ---------- CONTEXT ----------
class Account(BaseModel):
    name: str
    pin: int

# ---------- INPUT GUARDRAIL ----------
class GuardrailOutput(BaseModel):
    is_bank_related: bool

guardrail_agent = Agent(
    name="Guardrail Agent",
    instructions="You are a guardrail agent. You check if the user is asking a bank-related question.",
    output_type=GuardrailOutput
)

@input_guardrail
async def check_bank_related(ctx: RunContextWrapper[None], agent: Agent, input: str) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    output_info = result.final_output
    tripwire = not output_info.is_bank_related  # Block if not bank related
    return GuardrailFunctionOutput(output_info=output_info, tripwire_triggered=tripwire)

# ---------- OUTPUT GUARDRAIL ----------
@output_guardrail
def block_sensitive_output(ctx: RunContextWrapper[None], agent: Agent, output: str) -> GuardrailFunctionOutput:
    # Prevent leaking account PIN or sensitive info
    if "PIN" in output or "password" in output.lower():
        return GuardrailFunctionOutput(output_info={"safe": False}, tripwire_triggered=True)
    return GuardrailFunctionOutput(output_info={"safe": True}, tripwire_triggered=False)

# ---------- TOOLS ----------
def check_user(ctx: RunContextWrapper[Account], agent: Agent) -> bool:
    return ctx.context.name == "Bisma" and ctx.context.pin == 5678

@function_tool(is_enabled=check_user)
def check_balance(account_number: str) -> str:
    return f"The balance of account {account_number} is 2,000,000 PKR"

@function_tool(is_enabled=check_user)
def transfer_money(to_account: str, amount: int) -> str:
    return f"Successfully transferred {amount} PKR to account {to_account}."

# ---------- HANDOFF AGENTS ----------
balance_agent = Agent(
    name="Balance Agent",
    instructions="You provide account balance when asked.",
    tools=[check_balance]
)

transfer_agent = Agent(
    name="Transfer Agent",
    instructions="You handle fund transfers between accounts.",
    tools=[transfer_money]
)

# ---------- MAIN BANK AGENT ----------
bank_agent = Agent(
    name="Bank Agent",
    instructions=(
        "You are a helpful bank agent. You can hand off to other agents "
        "for specific tasks like checking balance or transferring money."
    ),
    handoffs=[balance_agent, transfer_agent],
    input_guardrails=[check_bank_related],
    output_guardrails=[block_sensitive_output]
)

user_context = Account(name="Bisma", pin=5678)

def main():
    # Example 1: Balance check
    result1 = Runner.run_sync(bank_agent, "Check my balance for account 309473804",
                               context=user_context, run_config=config)
    print("\n--- Balance Check ---")
    print(result1.final_output)

    # Example 2: Fund transfer
    result2 = Runner.run_sync(bank_agent, "Transfer 5000 PKR to 123456789",
                               context=user_context, run_config=config)
    print("\n--- Fund Transfer ---")
    print(result2.final_output)

if __name__ == "__main__":
    main()
