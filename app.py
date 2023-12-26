from flask import Flask, render_template, request
from flask_cors import CORS
import requests
from telegram import Bot
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from telegram.ext import Updater

app = Flask(__name__)
CORS(app)

TELEGRAM_BOT_TOKEN = "6471724114:AAH7qsYVK-EVyxB3rXuV-5KpFq9JnVzTj34"
TELEGRAM_CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

updater = Updater(token=TELEGRAM_BOT_TOKEN)
dispatcher = updater.dispatcher

def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def send_to_telegram(ip, country):
    message = f"New visitor info:\nIP Address: {ip}\nCountry: {country}"
    updater.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

@app.route('/')
def index():
    ip_address = request.remote_addr
    country = get_country_by_ip(ip_address)
    send_to_telegram(ip_address, country)
    return render_template('index.html', ip=ip_address, country=country)

def get_country_by_ip(ip):
    response = requests.get(f'https://freegeoip.app/json/{ip}')
    data = response.json()
    country = data.get('country_name', 'Unknown')
    return country

if __name__ == '__main__':
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    updater.start_polling()
    app.run(debug=True)