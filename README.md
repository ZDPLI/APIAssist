# Мультимодальный медицинский чатбот

Веб‑приложение на Gradio, работающее через публичный туннель LocalTunnel к LM
Studio. Поддерживается мультимодальный ввод (текст и несколько изображений).
Все диалоги сохраняются между запусками, можно создавать несколько чатов.

## Запуск

1. Установите зависимости:

   ```bash
   python -m pip install -r requirements/requirements.txt
   ```

2. Создайте файл `.env` (пример ниже) или экспортируйте переменные окружения:

   - `LMSTUDIO_URL` — публичный URL LM Studio (например `https://example.loca.lt`)
     или `http://172.23.32.1:1234` при прямом подключении
   - `LMSTUDIO_API_KEY` — ключ (если требуется)
   - `LMSTUDIO_MODEL` — название модели
   - `SYSTEM_PROMPT` — системный промпт (необязательно)

3. Запустите LM Studio с моделью `lingshu-7b` и откройте доступ по нужному URL.

4. Запустите приложение:

   ```bash
   python app.py
   ```

Приложение будет доступно по адресу `http://<server>:7860`. Интерфейс оформлен в
стиле Material с зелёно‑синим акцентом. Ответы модели отображаются постепенно
в процессе генерации.

История диалогов хранится в файле `conversations.json` рядом с приложением.

## Пример `.env`

```bash
LMSTUDIO_URL=https://example.loca.lt
LMSTUDIO_API_KEY=lm-studio
LMSTUDIO_MODEL=lingshu-7b
SYSTEM_PROMPT=You are a helpful medical assistant.
```
