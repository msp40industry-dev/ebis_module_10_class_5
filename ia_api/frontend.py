import gradio as gr
import requests
import time
import os

# Modificar esta URL cuando queramos utilizar el multiagente
API_URL = os.getenv("API_URL", "http://localhost:8000/multiagent")
print(f"[LOG] Using API_URL={API_URL}")


def chat_with_markdown_stream(message, history):
    # Añadir mensaje del usuario con respuesta vacía inicialmente
    history = history + [{"role": "user", "content": message}, {"role": "assistant", "content": ""}]
    yield "", history, history

    # Preparamos payload - convertir historial a formato esperado por el backend
    backend_history = []
    for msg in history[:-1]:  # Excluir el último mensaje vacío que acabamos de añadir
        if msg["content"]:  # Solo incluir mensajes no vacíos
            backend_history.append({"role": msg["role"], "content": msg["content"]})
    
    payload = {"user_input": message, "history": backend_history}
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        response.raise_for_status()
        full_reply = response.json().get("result", "[Sin respuesta del backend]")
        
        # Simular streaming local palabra por palabra, mejora la UX
        bot_reply = ""
        for word in full_reply.split(" "):
            bot_reply += word + " "
            history[-1] = {"role": "assistant", "content": bot_reply}
            yield "", history, history
            time.sleep(0.02)  # efecto de typing
    except Exception as e:
        bot_reply = f"[Error contactando backend: {e}]"
        history[-1] = {"role": "assistant", "content": bot_reply}
        yield "", history, history

with gr.Blocks(theme="soft") as demo:
    gr.Markdown("## 💬 Chatbot — Markdown con efecto de streaming")

    chatbot = gr.Chatbot(label="Chatbot (Markdown)")
    msg = gr.Textbox(placeholder="Escribe tu mensaje...", label="Tu mensaje")
    state = gr.State([])

    msg.submit(
        chat_with_markdown_stream,
        inputs=[msg, state],
        outputs=[msg, chatbot, state]
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, server_name="0.0.0.0", share=True)