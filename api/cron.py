from apscheduler.schedulers.background import BackgroundScheduler
from .transaction import new_transaction_request
import atexit
scheduler = BackgroundScheduler()
scheduler.add_job(func=new_transaction_request, trigger="interval", seconds=60)
atexit.register(lambda: scheduler.shutdown())

