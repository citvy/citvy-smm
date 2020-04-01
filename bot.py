import os
import main
import config
import telebot
import requests
import evaluate

bot = telebot.TeleBot(config.token)

UPLOAD_FOLDER = os.getcwd() + '\\examples\\'
DOWNLOAD_FOLDER = os.getcwd() + '\\examples\\thumbs\\'

@bot.message_handler(commands=["start"])
def hello(message):
    bot.send_message(message.chat.id, f"Привет {message.from_user.first_name} я CITVY BOT!\nЯ помогу вас сделать красивые артворки\nскиньте картинку как файл потом текст и получите готовый картинок")

@bot.message_handler(content_types=["photo"])
def get_photo(message):
    bot.send_message(message.chat.id, "Пожалуйста скиньте картинку как файл")

@bot.message_handler(content_types=["document"])
def get_photo(message):
    config.in_file = message.document.file_name
    config.out_file = f"converted_{message.document.file_name}"
    file_id = message.document.file_id
    url = f"https://api.telegram.org/bot{config.token}/getFile?file_id={file_id}"
    response = requests.get(url)
    file_path = response.json()['result']['file_path']
    url = f"https://api.telegram.org/file/bot{config.token}/{file_path}"
    response = requests.get(url)
    with open(UPLOAD_FOLDER + config.in_file, "wb") as photo:
        photo.write(response.content)
    bot.send_message(message.chat.id, "Хорошо! Сейчас пишите текст который будет находится на картинке")

@bot.message_handler(content_types=["text"])
def get_text(message):
    config.text = message.text
    if config.in_file and config.out_file and config.text:
        evaluate.ins = UPLOAD_FOLDER + config.in_file
        evaluate.outs = DOWNLOAD_FOLDER + config.out_file
        evaluate.main()
        main.make_artwork(evaluate.outs, evaluate.outs, config.text)
        with open(DOWNLOAD_FOLDER + config.out_file, "rb") as photo:
            bot.send_photo(message.chat.id, photo.read())
        # os.system(f"rm {evaluate.ins} {evaluate.outs} {DOWNLOAD_FOLDER + config.out_file, config.text}") """for UNIX systems [MacOS, Linux]"""
        config.in_file = None
        config.out_file = None
        config.text = None
        evaluate.ins = None
        evaluate.out = None

bot.polling()
