import os 
from dotenv import load_dotenv

load_dotenv()

import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
# print("BOT_TOKEN:", BOT_TOKEN)  # Add this line for debugging

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "how are you doing?")
    
    
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    
bot.infinity_polling()
