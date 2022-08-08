import requests
class Telegram:
    def __init__(self,token,proxy):
        self.token=token
        self.proxy=proxy
        self.setwebhook_url()
    def setwebhook_url(self):
        url=f'https://api.telegram.org/bot{self.token}/setWebhook?url={self.proxy}'
        print(url)
        requests.get(url)
    
    def parse_message(self,message):
        print("message-->",message)
        chat_id = message['message']['chat']['id']
        txt = message['message']['text']
        print("chat_id-->", chat_id)
        print("txt-->", txt)
        return chat_id,txt

    def tel_send_message(self,chat_id, text):
        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {
                    'chat_id': chat_id,
                    'text': text
                    }
        r = requests.post(url,json=payload)
        return r
