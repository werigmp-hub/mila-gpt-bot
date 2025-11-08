import os
import threading
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import openai

# -------------------------
# 1️⃣ Получаем ключи из Environment
# -------------------------
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN:
    raise ValueError("Bot token is not defined! Set TELEGRAM_BOT_TOKEN in Environment variables.")
if not OPENAI_KEY:
    raise ValueError("OpenAI API key is not defined! Set OPENAI_API_KEY in Environment variables.")

# -------------------------
# 2️⃣ Настраиваем OpenAI
# -------------------------
openai.api_key = OPENAI_KEY

def ask_openai(question: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# -------------------------
# 3️⃣ Настраиваем Telegram бота
# -------------------------
bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Я ваш бот с OpenAI 🤖")

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    answer = ask_openai(user_text)
    update.message.reply_text(answer)

updater.dispatcher.add_handler(CommandHandler("start", start))
updater.dispatcher.add_handler(CommandHandler("help", start))  # Для примера
updater.dispatcher.add_handler(updater.dispatcher.add_handler(
    lambda update, context: handle_message(update, context)
))

# Запуск polling в отдельном потоке
threading.Thread(target=updater.start_polling, daemon=True).start()

# -------------------------
# 4️⃣ Настраиваем Flask
# -------------------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running! ✅"

# -------------------------
# 5️⃣ Запуск сервера
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


