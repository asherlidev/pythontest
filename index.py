from asyncio.windows_events import NULL
from tokenize import Token
from flask import Flask
from decouple import config
from flask import request
from flask import Response
# from api import schedule
from extern import extern
from api import scheduler
import time
app=Flask(__name__)
# global variable

telegram=extern.telegram
@app.route('/',methods=['GET','POST'])
def index():
    if request.method =="POST":
         msg = request.get_json()
         chat_id,txt = telegram.parse_message(msg)
         print(txt)
         telegram.tel_send_message(chat_id,"Received your message")  
         if chat_id not in extern.chatid_arr:
            extern.chatid_arr.append(chat_id)
         return Response('ok', status=200)      
       
    else:
          return "<h1>Welcome!</h1>"

if __name__=='__main__':   
    telegram.setwebhook_url()
    scheduler.start()
    app.run(threaded=True, port=config('PORT'))
  