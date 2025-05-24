import asyncio
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
import system

# Initialize MCP client
token = load_dotenv("github_token")
google_api_key = load_dotenv("google_api_key")
mcp = MultiServerMCPClient({
    "github": {
        "command": "python",
        "args": ["./github.py"],
        "transport": "stdio",
    }
})

# Fetch tools from MCP server
async def get_tools():
    tools = await mcp.get_tools()
    return tools

tools = asyncio.run(get_tools())

# System prompt template that includes tool information

class Agent:
    def __init__(self, system_prompt=system.prompt):
        # Format system prompt with available tools
        self.prompt = system_prompt.format(tools="\n".join([f"- {tool}" for tool in tools]))
        self.chat_client = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=google_api_key,
            temperature=0
        )
        self.memory = [system_message(self.prompt)()]
        self.mcp = mcp

    async def execute_tool(self, tool_name: str, args: list) -> str:
        """Execute a tool via the MCP client."""
        try:
            # Call the tool using the MCP client
            tool = [tool for tool in tools if tool.name==tool_name][0]
            result = tool.run(args[0])
            # Check if the result is a dictionary and format it
            return str(result)
        except Exception as e:
            return f"Error executing tool {tool_name}: {str(e)}"

    def execute(self, prompt: str) -> str:
        """Execute a single interaction with the model."""
        self.memory.append(user_message(prompt)())
        result = self.chat_client.invoke(self.memory)
        self.memory.append(assistant_message(result.content)())
        return result.content

    async def query(self, prompt: str, max_loops: int = 5) -> str:
        """Handle a query with potential tool execution."""
        tool_regex = re.compile(r'Tool: (\w+): (.*)')
        i = 0
        next_prompt = prompt

        while i < max_loops:
            i += 1
            result = self.execute(next_prompt)
            print(f"Model response: {result}")

            # Check if the response contains an action
            action_match = tool_regex.search(result.strip())
            if action_match:
                tool_name = action_match.group(1)
                args = [arg.strip() for arg in action_match.group(2).split(",") if arg.strip()]
                
                # Verify tool exists
                if tool_name not in [tool.name for tool in tools]:
                    self.memory.append(assistant_message(f"Error: Tool {tool_name} not found.")())
                    return f"Tool {tool_name} not found."

                # Execute the tool
                observation = await self.execute_tool(tool_name, args)
                print(f"Tool {tool_name} result: {observation}")
                
                # Feed the observation back as the next prompt
                next_prompt = f"Observation: {observation}"
                self.memory.append(user_message(next_prompt)())
            else:
                # No action found, return the result
                return result

        return "Max loops reached without a final answer."

# Message classes
class user_message:
    def __init__(self, message):
        self.message = message

    def __call__(self):
        return {"role": "user", "content": self.message}

class assistant_message:
    def __init__(self, message):
        self.message = message

    def __call__(self):
        return {"role": "assistant", "content": self.message}

class system_message:
    def __init__(self, message):
        self.message = message

    def __call__(self):
        return {"role": "system", "content": self.message}

# Example usage
async def main():
    agent = Agent()
    result = await agent.query("Get information about the user 'octocat'")
    print(f"Final result: {result}")

if __name__ == "__main__":
    asyncio.run(main())