from token_telegram import TOKEN_TELEGRAM, TOKEN_CHAT_ID_ADMINS
import telepot
import sys
import time
import psutil

from telepot.loop import MessageLoop
from class_bot import BOT
from work_in_server import WorkInServer


bot = BOT(TOKEN_TELEGRAM)
bot.message_loop()
write_status = WorkInServer.get_instance('conn_client_proxy')

while 1:

    status_proxy = write_status.work()
    with open('status_proxy.txt', 'a') as f:
        f.write(str(status_proxy)+' ')

    time.sleep(10)