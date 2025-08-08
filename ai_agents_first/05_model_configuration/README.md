# 1. Async (Low-Level)
How it runs: Works in the background (you use await), so it doesn’t block other work.

Settings: You have to give all settings every time you run it.

Model: You tell it directly which AI model to use each time.

API Key/Client: You give it directly every time.

Reusability: Low — because everything is hardcoded.

Tracing (logging): You must turn it off manually.

# 2. Run-Level Config
How it runs: Runs normally (step-by-step), not in the background.

Settings: You use a RunConfig object that stores all settings for that run.

Model: Model info is inside the RunConfig.

API Key/Client: Comes from RunConfig.

Reusability: Medium — you can reuse the same RunConfig for different runs.

# 3. Global Config
How it runs: Runs normally (step-by-step).

Settings: Set once globally; works for all runs.

Model: Model is already set globally; you don’t have to pass it again.

API Key/Client: Set once and used everywhere.

Reusability: High — works in any part of the code.

Tracing: Can be turned off globally for all runs.
Tracing: You can turn it off in the config.

## explain 
###  1. Async (Low-Level) Version
```
async def main():
    agent = Agent(..., model=OpenAIChatCompletionsModel(...))
    result = await Runner.run(agent, "...")
```
✅ What this means:

You’re using asyncio → runs in the background without stopping other code.

Every time, you have to manually set up the client, model, and agent.

To get the result, you use await.

Good for: quick testing, maximum flexibility, or one-time runs.

❌ Downside:

Not reusable — you must write all the setup again every time.

### 2. Run-Level Config Version
```
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
result = Runner.run_sync(agent, ..., run_config=config)
```
In this:

You make a RunConfig that stores:

Model

Client (provider)

Tracing settings

The model is not given directly to the agent — it comes from the config.

Uses run_sync(...), so no async needed.

✅ Advantages:

The same RunConfig can be reused with multiple agents.

Centralized settings → less repeated code.

❌ Downside:

You still need some setup in every script.

### 3. Global Config Version
```
set_default_openai_client(...)
set_default_openai_api(...)
set_tracing_disabled(...)
```
In this:

You set up everything globally:

Client

API type (e.g., "chat_completions")

Tracing turned off

In the agent, you only give the model name.
```
Agent(..., model="gemini-2.0-flash")
```
Now these default settings are applied everywhere automatically.

✅ Advantages:

Most reusable and clean setup.

Client and model set in one place → later you only write the agent and prompt.

❌ Downside:

Not good if you need different clients/models in the same script.
When to Use Which?

Learning / Experimenting: Use Async Low-Level

Medium apps / Running the same agent multiple times: Use RunConfig

Production / Large projects: Use Global Config

### Final Summary

Async: You manually set up everything (client, model, agent) and use await.

RunConfig: You make one config object that stores all settings, and the agent uses it.

Global: You set up everything once globally, then later you only write the agent and prompt.
