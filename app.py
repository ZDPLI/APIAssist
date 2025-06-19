"""Gradio chat client for LM Studio.

This application provides a multimodal chat interface that sends user
messages and optional images to LM Studio via its OpenAI-compatible API.
Conversation histories are stored on disk so multiple chats can be
continued between runs.
"""
import os
from typing import Dict, List, Tuple, Iterable, Optional
load_dotenv()
LMSTUDIO_URL = os.getenv("LMSTUDIO_URL", "http://172.23.32.1:1234")
LMSTUDIO_API_KEY = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
LMSTUDIO_MODEL = os.getenv("LMSTUDIO_MODEL", "lingshu-7b")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "")

CHAT_ENDPOINT = LMSTUDIO_URL.rstrip("/") + "/v1/chat/completions"
Conversation = List[Tuple[str, str]]
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

def _build_messages(text: str, image_path: Optional[str], history: Conversation) -> List[Dict]:
    messages: List[Dict] = []
    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})
        content = [
            {"type": "text", "text": text or ""},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
        ]
        messages.append({"role": "user", "content": content})
    return messages

def chat_with_lmstudio(text: str, image_path: Optional[str], history: Conversation, stream: bool) -> Iterable[str]:
    payload = {
        "model": LMSTUDIO_MODEL,
        "messages": _build_messages(text, image_path, history),
        "stream": stream,
    }
    headers = {"Authorization": f"Bearer {LMSTUDIO_API_KEY}"}
    resp = requests.post(CHAT_ENDPOINT, json=payload, headers=headers, stream=stream, timeout=90)

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        yield content
        return

            chunk = line.decode().split("data:", 1)[1].strip()
            if chunk == "[DONE]":
            delta = json.loads(chunk)["choices"][0]["delta"]

def respond(message: str, image: Optional[str], chat_id: str, convs: Conversations):

    collected = ""
        for token in chat_with_lmstudio(message, image, history[:-1], stream=True):
            collected += token
            history[-1] = (message, collected)

def change_chat(chat_id: str, convs: Conversations):

def new_chat(convs: Conversations):


    current_chat = gr.State(current_cid)
            conv_select = gr.Dropdown(label="Диалоги", choices=list(conversations.keys()), value=current_cid)
            chatbot = gr.Chatbot(value=conversations[current_cid], elem_classes="chatbot")
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
