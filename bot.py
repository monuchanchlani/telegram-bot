import os
import telebot

# Get the bot token from Render environment variables
BOT_TOKEN = os.getenv("7583172405:AAGDad81jomlRIIDuYmh8TBmQF5s5cAyG70")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your Telegram bot.")

bot.polling()
