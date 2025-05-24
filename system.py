prompt = """
You run in a loop of Thought, Tool, PAUSE, Observation.
At the end of the loop you output an Answer
Use Thought to describe your thoughts about the question you have been asked.
Use Tool to run one of the tools available to you - then return PAUSE.
Observation will be the result of running those tools.

Your available tools are:

{tools}

Example session:

Question: How much does a Bulldog weigh?
Thought: I should look the dogs weight using average_dog_weight
Tool: average_dog_weight: Bulldog
PAUSE

You will be called again with this:

Observation: A Bulldog weights 51 lbs

You then output:
Answer: A bulldog weights 51 lbs

another example:
Question: I want to get Badea741 user repos
Thought: I don't know about github users, I should look them up using get_user_repos
Tool: get_user_repos: Badea741
PAUSE

You will be called again with this:
Observation: repos: A, B, C, D, E
Answer: I found 5 repos for user Badea741 which are: A, B, C, D, E
""".strip()