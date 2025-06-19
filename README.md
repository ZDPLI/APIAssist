# Мультимодальный медицинский чатбот

Небольшое веб-приложение на Gradio, позволяющее общаться с локальной моделью LM Studio, доступной по адресу `http://172.23.32.1:1234` или `http://localhost:1234`. Поддерживается отправка текста и одного изображения в сообщении.

## Запуск

1. Установите зависимости:

```bash
python -m pip install -r requirements/requirements.txt
```

2. Создайте файл `.env` (см. пример ниже) или экспортируйте переменные окружения:

- `LMSTUDIO_URL` — URL LM Studio (порт 1234), например `http://172.23.32.1:1234` или `http://localhost:1234`
- `LMSTUDIO_API_KEY` — ключ (если не требуется, оставьте `lm-studio`)
- `LMSTUDIO_MODEL` — название модели в LM Studio
- `SYSTEM_PROMPT` — системный промпт (опционально)

3. Запустите приложение:

```bash
python app.py
```

Интерфейс будет доступен по адресу `http://<server>:7860`.

## Пример `.env`

```bash
LMSTUDIO_URL=http://172.23.32.1:1234
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=lingshu-7b
SYSTEM_PROMPT=You are a helpful medical assistant.
```
