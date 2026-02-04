from langchain.agents import create_agent
from langchain_tavily import TavilySearch
from dotenv import dotenv_values

env_variables = dotenv_values()
web_search = TavilySearch(max_results=3, tavily_api_key=env_variables["TAVILY_API_KEY"])

research_agent = create_agent(
    model="openai:gpt-4.1",
    tools=[web_search],
    system_prompt=(
        "You are a research agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with research-related tasks, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="research_agent",
)