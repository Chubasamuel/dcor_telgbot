from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup,MessageEntity
import requests
import re
import logging
import os
import sys

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
channel= os.getenv("CHANNEL")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",port=PORT,url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def send_doc(f_id):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id
    r=requests.post(url,headers={"enctype":"multipart/form-data"})
def send_docByUrl(f_id):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id
    r=requests.get(url)
def file_id_gt(bot,update):
    file_id_g=update.message.document.file_id
    send_doc(file_id_g)
def file_id_gt2(bot,update):
    file_id_g=update.message.text
    send_docByUrl(file_id_g)
def echo(bot, update):
    print(update.message.chat_id)
    print(update.message.text)
def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
def boop(bot,update):
    update.message.reply_text("Wait I don't know anything yet")
if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('do',boop))
    dp.add_handler(MessageHandler(Filters.document,file_id_gt))
    dp.add_handler(MessageHandler(Filters.text&(Filters.entity(MessageEntity.URL)|Filters.entity(MessageEntity.TEXT_LINK)),file_id_gt2))
    run(updater)
