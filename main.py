import telebot
import requests
import time
from flask import Flask
import threading
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Mila bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я Мила 🤖 — твой ИИ-помощник. Задай вопрос!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENAI_KEY}"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": message.text}]
        }
        r = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response = r.json()["choices"][0]["message"]["content"]
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

def run_bot():
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            print(f"Ошибка polling: {e}")
            time.sleep(5)

# Запускаем Flask и бота в разных потоках
threading.Thread(target=run_flask).start()
run_bot()

