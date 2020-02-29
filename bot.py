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
def start_handler(bot, update):
    # Creating a handler-function for /start command 
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Hello from Python!\nPress /random to get random number")

def get_url():
    contents = requests.get('https://random.dog/woof.json').json()
    url = contents['url']
    return url
def get_send(f_id):

    f="Pediatric Acute Lymphoblastic Leukemia Workup_ Approach Considerations, Immunophenotyping, Cytogenetic and Molecular Studies.pdf"
    token="1076744419:AAH3Ih_bZeRPTZDVec3q0eOFTmaEFiGk6TI"
  #  channel2="1076744419"
    channel="@dcor_botTest"
    message="Works fine? Good"
    message=f
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id
    #"BQACAgQAAxkBAAEnBfJeWRfV3TslAVPm62OJZeMxaWdTggAC3QYAAme0yFLYyEOXUjOjpxgE"
    url2="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+channel+"&text="+f
    #url3="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+channel2+"&text="+"bop"
    r=requests.post(url,headers={"content-type":"application/pdf","enctype":"multipart/form-data"})
   # r=requests.get(url2,headers={"content-type":"text/plain"})
    #r=requests.get(url3,headers={"content-type":"text/plain"})
    #print("type of r--->",type(r),"\nr--->",r)
    #for i in r:
       # print(i,"--->",r[i],"\n")
def file_id_gt(bot,update):
    #get_send()
    file_id_g=update.message.document.file_id
    get_send(file_id_g)
    print("----___-")
    print(file_id_g)
def file_id_gt2(bot,update):
    #get_send()
    file_id_g=update.message.text
    #chat_id=update.message.chat_id
   # bot.sendDocument(chat_id=chat_id,document=file_id_g)
    get_send(file_id_g)
    print("----___-")
    print(file_id_g)
  #  f=open("file_id.txt","a+")
  #  f.write(file_id_g)
 #   f.close()
def echo(bot, update):
    print(update.message.chat_id)
    print(update.message.text)
    #context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
def boop(bot,update):
    f="Pediatric Acute Lymphoblastic Leukemia Workup_ Approach Considerations, Immunophenotyping, Cytogenetic and Molecular Studies.pdf"
    #get_send();
    chat_id=update.message.chat_id
    #chat_id="@dcor_helper_telgbot"
    #chat_id="994850954"
    bot.sendDocument(chat_id=chat_id,document=open(f,"rb"))
    update.message.reply_text(f)
    print("Chat ID:: ",update.message.chat_id)
if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('send_med_book',boop))
    dp.add_handler(MessageHandler(Filters.document,file_id_gt))
    dp.add_handler(MessageHandler(Filters.text&(Filters.entity(MessageEntity.URL)|Filters.entity(MessageEntity.TEXT_LINK)),file_id_gt2))
    run(updater)
