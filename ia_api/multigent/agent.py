from typing import Annotated

from langchain_core.tools import tool, InjectedToolCallId
from langgraph.prebuilt import InjectedState
from langgraph.graph import StateGraph, START, MessagesState, END
from langgraph.types import Command
from langchain.agents import create_agent

from multiagent.math import math_agent
from multiagent.research import research_agent



# def create_handoff_tool(*, agent_name: str, description: str | None = None):
#     """Implementaremos los traspasos mediante handoff tools, y proporcionaremos estas herramientas al agente supervisor:
#      cuando el supervisor invoque estas herramientas, traspasará el control a un agente trabajador, pasando el historial
#       completo de mensajes a ese agente."""
#
#     name = f"transfer_to_{agent_name}"
#     description = description or f"Ask {agent_name} for help."
#
#     @tool(name, description=description)
#     def handoff_tool(
#         state: Annotated[MessagesState, InjectedState],
#         tool_call_id: Annotated[str, InjectedToolCallId],
#     ) -> Command:
#         tool_message = {
#             "role": "tool",
#             "content": f"Successfully transferred to {agent_name}",
#             "name": name,
#             "tool_call_id": tool_call_id,
#         }
#         return Command(
#             goto=agent_name,
#             update={**state, "messages": state["messages"] + [tool_message]},
#             graph=Command.PARENT,
#         )
#
#     return handoff_tool
#
#
# # Handoffs
# assign_to_research_agent = create_handoff_tool(
#     agent_name="research_agent",
#     description="Assign task to a researcher agent.",
# )
#
# assign_to_math_agent = create_handoff_tool(
#     agent_name="math_agent",
#     description="Assign task to a math agent.",
# )
#
# # Creamos el agente supervisor
# supervisor_agent = create_agent(
#     model="openai:gpt-4.1",
#     tools=[assign_to_research_agent, assign_to_math_agent],
#     system_prompt=(
#         "You are a supervisor managing two agents:\n"
#         "- a research agent. Assign research-related tasks to this agent\n"
#         "- a math agent. Assign math-related tasks to this agent\n"
#         "Assign work to one agent at a time, do not call agents in parallel.\n"
#         "Do not do any work yourself."
#     ),
#     name="supervisor",
# )
#
# # Define the multi-agent supervisor graph
# supervisor = (
#     StateGraph(MessagesState)
#     # NOTE: `destinations` is only needed for visualization and doesn't affect runtime behavior
#     .add_node(supervisor_agent, destinations=("research_agent", "math_agent", END))
#     .add_node(research_agent)
#     .add_node(math_agent)
#     .add_edge(START, "supervisor")
#     # always return back to the supervisor
#     .add_edge("research_agent", "supervisor")
#     .add_edge("math_agent", "supervisor")
#     .compile()
# )
#
# # Generate the graph and save it to a file
# graph = supervisor.get_graph()
# png_data = graph.draw_mermaid_png()
#
# # Save to file
# with open("graph.png", "wb") as f:
#     f.write(png_data)

from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

supervisor = create_supervisor(
    model=init_chat_model("openai:gpt-4.1"),
    agents=[research_agent, math_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a research agent. Assign research-related tasks to this agent\n"
        "- a math agent. Assign math-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()