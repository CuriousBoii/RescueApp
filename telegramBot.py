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

#-------------------------------------------------------------kelage irodu tappide

def send_message(phone_number, message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
        }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f'Message sent to {phone_number} successfully!')
    else:
        print(f'Error sending message to {phone_number}: {response.text}')
