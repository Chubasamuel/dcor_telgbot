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
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&filename=yes_DCOR.pdf&document="+f_id
    r=requests.post(url,headers={"enctype":"multipart/form-data"})
def send_docByUrl(bot,update,f_id):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id+"&filename=Yes_DCOR.pdf"
    r=requests.get(url)
    if r.status_code!=200:
        update.message.reply_text("Sorry, seems no file was found at this url ---> "+f_id)
def send_docByUrl2(bot,update,f_id):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id+"&filename=Yes_DCOR.pdf"
    r=requests.get(url)
    if r.status_code!=200:
        errM="Sorry, seems no file was found at this url ---> "+f_id
        url="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+channel+"&text="+errM
        requests.get(url)
def file_id_gt(bot,update):
    file_id_g=update.message.document.file_id
    send_doc(file_id_g)
def file_id_gt2(bot,update):
    file_id_g=update.message.text
    if re.match(r'^https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx)$',file_id_g):
        send_docByUrl(bot,update,file_id_g)
    else:
        help_getBook2(bot,update,file_id_g)
def channel_getBookByUrl(bot,update):
    txt=update.message.text
    txt=re.sub("@dcorbot\s+","",txt)
    send_docByUrl(bot,update,txt)
def channel_getBookByUrl2(bot,update):
    txtt=update.channel_post.text
    txtt=re.sub("@dcorbot\s+","",txtt)
    help_getBook2(bot,update,txtt)
def help_getBook2(bot,update,txt):
    if re.match(r'^https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx)$',txt):
        send_docByUrl2(bot,update,txt)
    else:
        correctedText=re.search(r"url=https*://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx){1}",txt).group()
        correctedText=re.sub("url=","",correctedText)
        if re.match(r'^https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx)$',correctedText):
            send_docByUrl2(bot,update,correctedText)
        else:
            update.message.reply_text("Sorry, seems no file was found at this url ---> "+txt)
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
    dp.add_handler(MessageHandler(Filters.update.message&(Filters.entity(MessageEntity.URL)|Filters.entity(MessageEntity.TEXT_LINK)),file_id_gt2))
    dp.add_handler(MessageHandler(Filters.update.channel_posts&Filters.regex(r'^@dcorbot\s+https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx)$'),channel_getBookByUrl))
    dp.add_handler(MessageHandler(Filters.update.channel_posts&Filters.regex(r'^@dcorbot\s+https{0,1}://.+'),channel_getBookByUrl2))
    run(updater)
