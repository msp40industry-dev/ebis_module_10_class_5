from fastapi import FastAPI
from chatbot_agent.agent import graph
from chatbot_agent.utils import RequestData
from multiagent.agent import supervisor
from multiagent.utils import pretty_print_messages


app = FastAPI()

@app.post("/chatbot")
async def chatbot(data: RequestData):
    """
    Endpoint stateless: recibe el historial del frontend y lo reenvía al LLM.
    """
    state = {"user_input": data.user_input, "history": data.history}
    result = graph.invoke(state)
    return {"result": result["answer"], "history": result["history"]}

# TODO - create new endpoint with multiagent

@app.post("/multiagent")
async def multiagent(data: RequestData):
    """
    Endpoint stateless: recibe el historial del frontend y lo reenvía al LLM.
    """
    # "find US and New York state GDP in 2024. what % of US GDP was New York state?",
    # "who is the mayor of NYC?"

    for chunk in supervisor.stream({"messages": [{"role": "user", "content": data.user_input}]}):
        pretty_print_messages(chunk, last_message=True)

    final_message_history = chunk["supervisor"]["messages"]
    final_message = final_message_history[-1].content

    return {"result": final_message, "history": final_message_history}