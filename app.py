"""Multimodal chat client for LM Studio.

This Gradio application sends text and image prompts to LM Studio using its
OpenAI-compatible API and streams the response. Conversation histories are
stored on disk so chats can be resumed between runs.
"""
from __future__ import annotations

import os
import re
from typing import Dict, Iterable, List, Optional
import requests
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://172.23.32.1:1234")
LMSTUDIO_API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "lingshu-7b")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "")
MAX_NUM_IMAGES = int(os.getenv("MAX_NUM_IMAGES", "5"))

CHAT_ENDPOINT = LMSTUDIO_URL.rstrip("/") + "/v1/chat/completions"
Message = Dict[str, object]
Conversation = List[Message]
Conversations = Dict[str, Conversation]

def load_conversations() -> Conversations:
        try:
            with open(CONV_FILE, "r", encoding="utf-8") as f:
        except Exception:
            pass
def save_conversations(convs: Conversations) -> None:
    with open(CONV_FILE, "w", encoding="utf-8") as f:
        json.dump(convs, f, ensure_ascii=False, indent=2)


conversations: Conversations = load_conversations()
if conversations:
    current_cid = list(conversations.keys())[0]
    current_cid = time.strftime("%Y%m%d-%H%M%S")
    conversations[current_cid] = []
    save_conversations(conversations)

# ---------------------------------------------------------------------------
# Helpers for converting user input to LM Studio format
# ---------------------------------------------------------------------------

def _encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def process_user_message(message: dict) -> object:
    """Convert textbox output to OpenAI message content."""
    text = message.get("text", "")
    files: List[str] = message.get("files") or []
    if not files:
        return text

    if len(files) > MAX_NUM_IMAGES:
        raise ValueError(f"You can upload up to {MAX_NUM_IMAGES} images.")

    if "<image>" in text:
        parts = re.split(r"(<image>)", text)
        content: List[dict] = []
        idx = 0
        for part in parts:
            if part == "<image>" and idx < len(files):
                b64 = _encode_image(files[idx])
                content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
                idx += 1
            elif part and part != "<image>":
                content.append({"type": "text", "text": part})
        return content

    content = []
    if text:
        content.append({"type": "text", "text": text})
    for path in files:
        b64 = _encode_image(path)
        content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}})
    return content


# ---------------------------------------------------------------------------
# LM Studio communication
# ---------------------------------------------------------------------------

def chat_with_lmstudio(messages: Conversation, stream: bool, max_tokens: int) -> Iterable[str]:
        "messages": messages,
        "max_tokens": max_tokens,
    resp.raise_for_status()
        yield data.get("choices", [{}])[0].get("message", {}).get("content", "")

# ---------------------------------------------------------------------------
# Gradio callbacks
# ---------------------------------------------------------------------------

def respond(message: dict, chat_id: str, convs: Conversations, system_prompt: str, max_tokens: int):
    history = convs.setdefault(chat_id, [])
    user_content = process_user_message(message)
    history.append({"role": "user", "content": user_content})
    convo_for_api = []
    if system_prompt:
        convo_for_api.append({"role": "system", "content": system_prompt})
    convo_for_api.extend(history)

    assistant = {"role": "assistant", "content": ""}
        for token in chat_with_lmstudio(convo_for_api, stream=True, max_tokens=max_tokens):
            assistant["content"] = collected
            yield history + [assistant], None, convs
    except Exception as exc:
        assistant["content"] = f"Error: {exc}"
        yield history + [assistant], None, convs
        history.append(assistant)
        save_conversations(convs)
        return

    history.append(assistant)
    yield history, None, convs


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------

with gr.Blocks(theme=theme, css="style.css") as demo:

            conv_select = gr.Dropdown(label="Диалоги", choices=list(conversations.keys()), value=current_cid)
            chatbot = gr.Chatbot(value=conversations[current_cid], elem_classes="chatbot", type="messages")
            with gr.Row():
                txt = gr.MultimodalTextbox(file_types=["image"], file_count="multiple", label="Сообщение", autofocus=True)
                send = gr.Button("Отправить")
            sys_prompt = gr.Textbox(label="System Prompt", value=SYSTEM_PROMPT)
            max_tokens = gr.Slider(label="Max Tokens", minimum=100, maximum=4096, value=2048, step=10)

    send.click(respond, [txt, current_chat, conv_state, sys_prompt, max_tokens], [chatbot, txt, conv_state], queue=True)

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
    return gr.update(choices=list(convs.keys()), value=chat_id), [], convs, chat_id
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
