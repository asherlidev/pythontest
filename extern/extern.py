from telegram import Telegram
from decouple import config
TOKEN=config('TOKEN')
PROXY=config('DOMAIN_NAME')
telegram= Telegram(TOKEN,PROXY)
chatid_arr=[]