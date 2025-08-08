# 1. Async (Low-Level)
How it runs: Works in the background (you use await), so it doesn’t block other work.

Settings: You have to give all settings every time you run it.

Model: You tell it directly which AI model to use each time.

API Key/Client: You give it directly every time.

Reusability: Low — because everything is hardcoded.

Tracing (logging): You must turn it off manually.

#2. Run-Level Config
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

