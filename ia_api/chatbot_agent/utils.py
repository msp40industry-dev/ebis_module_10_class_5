from tenacity import retry, wait_exponential, stop_after_attempt
from pydantic import BaseModel, constr
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import dotenv_values

env_variables = dotenv_values()
llm = ChatOpenAI(model="gpt-4o-mini", api_key=env_variables["OPENAI_API_KEY"])

# GESTIÓN DE ERRORES Y TIMEOUTS
# La API del LLM puede fallar o dar timeout, lo capturamos dentro de un try/except

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def safe_invoke_llm(messages):
    """
    Puede recibir:
      - string simple ("Hola")
      - lista de mensajes [{"role": "user"/"assistant"/"system", "content": "..."}]
    """
    if isinstance(messages, str):
        messages = [HumanMessage(content=messages)]
    else:
        formatted = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                formatted.append(HumanMessage(content=content))
            elif role == "assistant":
                formatted.append(AIMessage(content=content))
            elif role == "system":
                formatted.append(SystemMessage(content=content))
        messages = formatted

    return llm.invoke(messages)

def answer_question(state: dict) -> dict:
    user_input = state["user_input"]
    try:
        response = safe_invoke_llm(user_input)
        logger.info(f"[BACKEND] Respuesta generada: {response[:50]}...")
        return {"answer": response.content}
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}


# VALIDACIÓN DEL INPUT
# No queremos que se envíen inputs enormes, añadimos limitaciones usando pydantic

class RequestData(BaseModel):
    user_input: constr(min_length=1, max_length=500)  # limit input size
    history: list[dict] = []  # historial completo del frontend

# LOGGEO
# Añadimos loggeo de los resultados para aportar visibilidad

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def answer_question(state: dict) -> dict:
    logger.info(f"Received input: {state['user_input']}")
    response = safe_invoke_llm(state['user_input'])
    logger.info("LLM response generated")
    return {"answer": response.content}