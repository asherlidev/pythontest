from email import message
import requests
from decouple import config
import calendar
import time
from extern import extern
import aiohttp
import asyncio
ADDRESS=config('ADDRESS')
start=False
telegram = extern.telegram
start_time_stamp=""
end_time_stamp=""
def get_time_stamp():
    time_stamp = int(round(time.time() * 1000))
    return time_stamp
async def transaction_account():
    url=f'https://apilist.tronscan.org/api/account?address={ADDRESS}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp :
            res = await resp.json()
            for x in res['tokens']:
                message="previous USDT transaction summary"
                if x['tokenAbbr'] == "USDT":
                    message+="amount:"+str(x['amount'])+"\n"
                    message+="balance:"+x['balance']+"\n"
                    message+="nrOfTokenHolders:"+str(x['nrOfTokenHolders'])+"\n"
                    message+="tokenPriceInTrx:"+str(x['tokenPriceInTrx'])+"\n"
                    message+="transferCount:"+str(x['transferCount'])+"\n"
                    for chatid in extern.chatid_arr:
                        
                        telegram.tel_send_message(chatid,message)
async def transcan_api_request(url):
    global start_time_stamp
    global end_time_stamp
    message_item=""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            res=await resp.json()
            print(res)
            token_transfers=res['token_transfers']
            for trans_item in token_transfers:
                token_info=trans_item['tokenInfo']
                token_name=token_info['tokenAbbr']
                if token_name == "USDT":
                    message_item+="transaction_id:"+trans_item['transaction_id']+"\n"    
                    message_item+="approval_amount:"+str(trans_item['approval_amount'])+"\n"
                    message_item+="from_address:"+trans_item['from_address']+"\n"
                    message_item+="to_address:"+trans_item['to_address']+"\n"
            if len(token_transfers) > 0 :
                for chatid in extern.chatid_arr :
                    telegram.tel_send_message(chatid,message_item)        
            start_time_stamp = end_time_stamp
def new_transaction_request():
    for chatid in extern.chatid_arr:
        telegram.tel_send_message(chatid,"hello schedule job running")
    global start
    global start_time_stamp
    global end_time_stamp
    if not start:
        start = True
        start_time_stamp=get_time_stamp()
    else:
        end_time_stamp=get_time_stamp()
        url=f'https://apilist.tronscanapi.com/api/token_trc20/transfers?limit=20&start=0&contract_address={ADDRESS}'    
        url+="&start_timestamp="+str(start_time_stamp)
        url+="&end_timestamp="+str(end_time_stamp)
        url+="&confirm="
        print(url)
        asyncio.run(transaction_account())
        asyncio.run(transcan_api_request(url))
        # requests.get()