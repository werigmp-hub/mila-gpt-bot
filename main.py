from flask import Flask, request
import os
import telegram
import openai

# -------------------------
# 1️⃣ Переменные окружения
# -------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_KEY:
    raise ValueError("Переменные окружения не заданы!")

bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_KEY

app = Flask(__name__)

# -------------------------
# 2️⃣ Webhook для сообщений
# -------------------------
@app.route(f"/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    text = update.message.text

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        max_tokens=150
    )
    answer = response.choices[0].text.strip()
    bot.send_message(chat_id=chat_id, text=answer)
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

# -------------------------
# 3️⃣ Устанавливаем Webhook и запускаем Flask
# -------------------------
if __name__ == "__main__":
    url = os.environ.get("RENDER_EXTERNAL_URL")
    bot.setWebhook(f"{url}/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

