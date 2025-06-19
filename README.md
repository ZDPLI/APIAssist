# Мультимодальный медицинский чатбот

Веб-приложение на Gradio с материал-ориентированным дизайном. Оно позволяет
общаться с локальной моделью через **Ollama** (используйте `ollama run` или `ollama serve`) по адресу
`http://localhost:11434` (или другому, заданному в переменной окружения). Поддерживается отправка текста и изображения в одном
сообщении. Чаты сохраняются между запусками, можно вести несколько диалогов.

## Запуск

1. Установите зависимости:

```bash
python -m pip install -r requirements/requirements.txt
```

2. Создайте файл `.env` (см. пример ниже) или экспортируйте переменные окружения:

- `OLLAMA_URL` — URL Ollama (по умолчанию `http://localhost:11434`)
- `OLLAMA_API_KEY` — ключ (если Ollama запущена с `--api-key`)
- `OLLAMA_MODEL` — название модели в Ollama
- `SYSTEM_PROMPT` — системный промпт (опционально)

3. Убедитесь, что запущен `ollama serve` с моделью `hf.co/mradermacher/Bio-Medical-MultiModal-Llama-3-8B-V1-GGUF:Q8_0`:

```bash
ollama run hf.co/mradermacher/Bio-Medical-MultiModal-Llama-3-8B-V1-GGUF:Q8_0
```

4. Запустите приложение:

```bash
python app.py
```

Интерфейс будет доступен по адресу `http://<server>:7860` и оформлен в стиле
Material с зелёно‑синим акцентом. Ответы модели отображаются в режиме
стриминга – текст появляется по мере генерации.

Все диалоги сохраняются в файле `conversations.json` рядом с приложением.

## Пример `.env`

```bash
OLLAMA_URL=http://localhost:11434
OLLAMA_API_KEY=ollama
OLLAMA_MODEL=hf.co/mradermacher/Bio-Medical-MultiModal-Llama-3-8B-V1-GGUF:Q8_0
SYSTEM_PROMPT=You are a helpful medical assistant.
```
