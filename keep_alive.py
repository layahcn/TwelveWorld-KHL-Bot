from flask import Flask
from threading import Thread
import time
import pytz
import datetime

app = Flask('')

@app.route('/')
def home():
    now = time.time()
    timezone = pytz.timezone('Asia/Shanghai')
    localtime = datetime.datetime.fromtimestamp(now, timezone)
    ntime = localtime.strftime('%Y-%m-%d %H:%M:%S')
    return f"[{ntime}] Hello. I am alive!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()