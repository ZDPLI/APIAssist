"""Gradio chat client for a local Ollama server."""

import os
from dotenv import load_dotenv
load_dotenv()
import base64
import requests
import json
import time
import gradio as gr

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
API_KEY = os.environ.get("OLLAMA_API_KEY", "ollama")
MODEL = os.environ.get("OLLAMA_MODEL", "lingshu-7b")
SYSTEM_PROMPT = os.environ.get("SYSTEM_PROMPT")
CONV_FILE = "conversations.json"


def load_conversations():
    if os.path.exists(CONV_FILE):
        with open(CONV_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return {}
    return {}


def save_conversations(convs):
    with open(CONV_FILE, "w") as f:
        json.dump(convs, f)

if not OLLAMA_URL:
    raise RuntimeError("OLLAMA_URL environment variable not set")

CHAT_ENDPOINT = OLLAMA_URL.rstrip('/') + "/v1/chat/completions"
conversations = load_conversations()
if not conversations:
    cid = time.strftime("%Y%m%d-%H%M%S")
    conversations[cid] = []
    save_conversations(conversations)
else:
    cid = list(conversations.keys())[0]

def chat_with_ollama(text, image_path=None, history=None, stream=False):
    messages = []
    if SYSTEM_PROMPT:
        messages.append({"role": "system", "content": SYSTEM_PROMPT})
    user_content = []
    if text:
        user_content.append({"type": "text", "text": text})
    if image_path:
        with open(image_path, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
    messages.append({"role": "user", "content": user_content if len(user_content) > 1 else user_content[0]})

    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": stream,
    }
    headers = {"Authorization": f"Bearer {API_KEY}"}
    resp = requests.post(
        CHAT_ENDPOINT,
        json=payload,
        headers=headers,
        stream=stream,
        timeout=90,
    )
    resp.raise_for_status()
    if not stream:
        data = resp.json()
        return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    collected = ""
    for line in resp.iter_lines():
        if not line:
            continue
        if line.strip().startswith(b"data:"):
            content = line.decode().split("data:", 1)[1].strip()
            if content == "[DONE]":
                break
            delta = json.loads(content)["choices"][0]["delta"]
            token = delta.get("content")
            if token:
                collected += token
                yield token
    return collected

def respond(message, image, chat_id, convs):
    history = convs.get(chat_id, [])
    response = ""
    history.append((message, ""))
    convs[chat_id] = history
    save_conversations(convs)
    for token in chat_with_ollama(message, image, history, stream=True):
        response += token
        history[-1] = (message, response)
        yield history, "", None, convs
    save_conversations(convs)

def change_chat(chat_id, convs):
    return convs.get(chat_id, []), chat_id

def new_chat(convs):
    chat_id = time.strftime("%Y%m%d-%H%M%S")
    convs[chat_id] = []
    save_conversations(convs)
    return gr.Dropdown.update(choices=list(convs.keys()), value=chat_id), [], convs, chat_id

theme = gr.themes.Soft(primary_hue="green", secondary_hue="blue")

with gr.Blocks(theme=theme, css=".chatbot {height: 600px}") as demo:
    conv_state = gr.State(conversations)
    current_chat = gr.State(cid)
    with gr.Row():
        with gr.Column(scale=2):
            conv_select = gr.Dropdown(label="Диалоги", choices=list(conversations.keys()), value=cid)
            new_btn = gr.Button("Новый диалог")
        with gr.Column(scale=8):
            gr.Markdown("# Мультимодальный медицинский ассистент")
            chatbot = gr.Chatbot(value=conversations.get(cid, []), elem_classes="chatbot")
            with gr.Row(equal_height=True):
                txt = gr.Textbox(label="Сообщение", scale=8)
                img = gr.Image(type="filepath", label="Изображение", scale=2)
                send = gr.Button("Отправить", scale=1)

    send.click(respond, [txt, img, current_chat, conv_state], [chatbot, txt, img, conv_state], queue=True)
    conv_select.change(change_chat, [conv_select, conv_state], [chatbot, current_chat])
    new_btn.click(new_chat, conv_state, [conv_select, chatbot, conv_state, current_chat])

    demo.launch(server_name="0.0.0.0", server_port=7860)
