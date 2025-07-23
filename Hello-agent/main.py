from agents import Agent , Runner

agent= Agent(
    name = "Assistant",
    instructions= "are you halpfull assistant"
)

result = Runner.run_sync(agent , "Holle agent")
print (result.final_output)
