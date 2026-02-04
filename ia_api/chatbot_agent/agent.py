from langgraph.graph import StateGraph, START, END
from chatbot_agent.utils import logger, safe_invoke_llm


# 1 - Definimos el estado
class State(dict):
    user_input: str
    answer: str
    history: list[dict]


# 2 - Definimos la función que se ejecutará
def answer_question(state: dict) -> dict:

    user_input = state["user_input"]
    
    # Añadimos el nuevo mensaje al historial
    history = state.get("history", [])
    messages = history + [{"role": "user", "content": user_input}]

    logger.info(f"Input recibido: {state['user_input']}")

    # Llamamos al LLM con todo el contexto acumulado
    response = safe_invoke_llm(messages)
        
    # Devolvemos la respuesta + historial actualizado
    logger.info("Respuesta generada por el LLM")
    history.append({"role": "user", "content": user_input})
    history.append({"role": "assistant", "content": response.content})

    return {"answer": response.content, "history": history}


# 3 - Construímos el grafo
workflow = StateGraph(State)
workflow.add_node("answer", answer_question)
workflow.add_edge(START, "answer")
workflow.add_edge("answer", END)
graph = workflow.compile()