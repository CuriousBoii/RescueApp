from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = '7289555220:AAFvTN3j80yXf5FAzAaXRfvYG3mH-uNAi-I'
CHAT_ID = f'https://api.telegram.org/bot{BOT_TOKEN}/getChat?chat_id=@CodefuryCamp'

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your rescue bot.")

def main() -> None:
    builder = ApplicationBuilder().token("YOUR_TELEGRAM_BOT_TOKEN")
    builder.add_handler(CommandHandler("start", start))

    application = builder.build()
    application.run_polling()

def get_user_id(phone_number):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getUpdates'
    response = requests.get(url)
    updates = response.json()['result']
    for update in updates:
        if 'message' in update and 'contact' in update['message']:
            if update['message']['contact']['phone_number'] == phone_number:
                return update['message']['from']['id']
    return None


def add_volunteer_to_group(phone_number):
    user_id = get_user_id(phone_number)
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/addChatMember'
    data = {
        'chat_id': CHAT_ID,
        'user_id': user_id
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f'Volunteer {user_id} added to group successfully!')
    else:
        print(f'Error adding volunteer {user_id} to group: {response.text}')


import requests

def send_invite(phone_number):
    BOT_TOKEN = 'YOUR_BOT_TOKEN'
    CHAT_ID = 'YOUR_CHAT_ID'

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/exportChatInviteLink'
    params = {'chat_id': CHAT_ID}
    response = requests.get(url, params=params)
    invite_link = response.json()['result']


    send_message(phone_number, f'Join our Telegram group: {invite_link}')

#-------------------------------------------------------------Mele irodu tappide

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# importing os module for environment variables
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 

# accessing the bot token from .env file
botToken = os.getenv("BOT_TOKEN")
openaiToken = os.getenv("OPENAI_TOKEN")
#print("BOT_TOKEN = ", botToken)
#print("OPENAI_TOKEN = ", botToken)

# Creating OpenAI Client
from openai import OpenAI
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key = os.getenv("OPENAI_TOKEN"), base_url=base_url)

# Logging the updates. This helps in debugging the code.
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    BOT_TOKEN = 'YOUR_BOT_TOKEN'
    CHAT_ID = 'YOUR_CHAT_ID'

    url = f'https://api.telegram.org/bot{BOT_TOKEN}/exportChatInviteLink'
    params = {'chat_id': CHAT_ID}
    response = requests.get(url, params=params)
    invite_link = response.json()['result']
    reply = completion.choices[0].message.content
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token=botToken).build()
    
    start_handler = CommandHandler('ai', ai)
    application.add_handler(start_handler)
    
    application.run_polling()