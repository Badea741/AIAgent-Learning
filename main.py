import asyncio
import system
from agent import Agent

agent = Agent(system.prompt)

result =asyncio.run(agent.query("I want to get Badea741 user repos"))
result