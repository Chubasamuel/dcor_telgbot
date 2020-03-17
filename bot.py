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
def send_doc(f_id,f_capt):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    if len(f_capt)>0:
        part_url="&caption="+f_capt
    else:
        part_url=""
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id+part_url
    r=requests.post(url,headers={"enctype":"multipart/form-data"})
def send_docByUrl(bot,update,f_id,f_capt):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id+"&caption="+f_capt
    r=requests.get(url)
    if r.status_code!=200:
        update.message.reply_text("Sorry, seems no file was found at this url ---> "+f_id)
def send_docByUrl2(bot,update,f_id,f_capt):
    token=globals()["TOKEN"]
    channel=globals()["channel"]
    url="https://api.telegram.org/bot"+token+"/sendDocument?chat_id="+channel+"&document="+f_id+"&caption="+f_capt
    r=requests.get(url)
    if r.status_code!=200:
        errM="Sorry, seems no file was found at this url ---> "+f_id+"----"
        try:
            update.message.reply_text(errM)
        except:
            url="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+channel+"&text="+errM
            requests.get(url)
def getFilecaption(bot,update,f_id):
    ff=re.match("capt=.+\|\s+",f_id).group().strip()
    ff=re.sub("capt=","",ff)
    ff=ff[0:len(ff)-1]
    return ff
def file_id_gt(bot,update):
    file_id_g=update.message.document.file_id
    if update.message.caption:
        send_doc(file_id_g,update.message.caption)
    else:
        update.message.reply_text("No caption set.\nSending "+update.message.document.file_name+" without caption...")
        send_doc(file_id_g,"")
def file_id_gt2(bot,update):
    file_id_g=update.message.text
    if re.match(r'^capt=.+\|\s+https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub)$',file_id_g):
        file_caption=getFilecaption(bot,update,file_id_g)

        file_id_g=re.search(r"https*://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub){1}",file_id_g).group()
        send_docByUrl(bot,update,file_id_g,file_caption)
    else:
        help_getBook2(bot,update,file_id_g)
def channel_getBookByUrl(bot,update):
    txt=update.message.text
    txt=re.sub("@dcorbot\s+","",txt)
    file_caption=getFilecaption(bot,update,txt)
    txt=re.search(r"https*://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub){1}",txt).group()
    send_docByUrl(bot,update,txt,file_caption)
def channel_getBookByUrl2(bot,update):
    txtt=update.channel_post.text
    txtt=re.sub("@dcorbot\s+","",txtt)
    help_getBook2(bot,update,txtt)
def help_getBook2(bot,update,txt):
    file_caption=getFilecaption(bot,update,txt)
    if re.match(r'^https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub)$',txt):
        send_docByUrl2(bot,update,txt,file_caption)
    elif re.search(r'https*://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub).*',txt) and not "url=http" in txt:
        send_docByUrl2(bot,update,txt,file_caption)
    elif re.search(r'https*://t\.me.+',txt):
        send_docByUrl2(bot,update,txt,file_caption)
    else:
        correctedText=re.search(r"url=https*://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub){1}",txt).group()
        correctedText=re.sub("url=","",correctedText)
        if re.match(r'^https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub)$',correctedText):
            send_docByUrl2(bot,update,correctedText,file_caption)
        else:
            update.message.reply_text("Sorry, seems no file was found at this url ---> "+txt)
def bop(bot, update):
    url = get_url()
    chat_id = update.message.chat_id
    bot.send_photo(chat_id=chat_id, photo=url)
def boop(bot,update):
    update.message.reply_text("Wait I don't know what to do yet")
def cEcho(bot,update):                                    pass
def startBot(bot,update):
    msg="Hey, Good to meet you.\nWelcome To DCOR Telegram Bot.\nDesigned by Chuba Samuel,DCOR,\nI am meant to help you send medical resources to the medical library.\nEnter the /help command to see available helps"
    update.message.reply_text(msg)
def showHelp(bot,update):
    msg="Welcome\nEnter /bop command to get cool random dog pictures.\nEnter /help command to see this help again\n"
    msg+="\nUpload any resource here and I will send it to the channel immediately\n"
    msg+="\nTo send a resource through a link just type\n capt=The caption of the file| followed by the link\n"
    msg+="e.g\n   capt=Paediatric Textbook 4th Ed. | https://www.xz.bxxbbd.didj/jdjjf/paed.pdf\n"
    msg+="or e.g\n   capt=Anatomy Text| http://book.bk/jdjdhhdnd/anatomy.pdf/jdjdjjdeojrnfnf"
    update.message.reply_text(msg)
def cAll(bot,update):
    update.message.reply_text("---Gotten and Noted---")    
if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('bop',bop))
    dp.add_handler(CommandHandler('do',boop))
    dp.add_handler(CommandHandler('help',showHelp))
    dp.add_handler(CommandHandler('start',startBot))
    dp.add_handler(MessageHandler(Filters.update.channel_post,cEcho))
    dp.add_handler(MessageHandler(Filters.update.message.document&Filters.update.message.text,cAll))
    dp.add_handler(MessageHandler(Filters.document,file_id_gt))
    dp.add_handler(MessageHandler(Filters.update.message&(Filters.entity(MessageEntity.URL)|Filters.entity(MessageEntity.TEXT_LINK)),file_id_gt2))
    dp.add_handler(MessageHandler(Filters.update.channel_posts&Filters.regex(r'^@dcorbot\s+capt=.+\|\s+https{0,1}://.+(pdf|ppt|xls|xlsx|html|pptx|txt|doc|docx|epub)$'),channel_getBookByUrl))
    dp.add_handler(MessageHandler(Filters.update.channel_posts&Filters.regex(r'^@dcorbot\s+capt=.+\|\s+https{0,1}://.+'),channel_getBookByUrl2))
    run(updater)
