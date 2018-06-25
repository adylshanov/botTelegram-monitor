import telepot
import psutil
import collections
import re
import subprocess
from datetime import datetime

import time
from telepot.loop import MessageLoop

from token_telegram import TOKEN_TELEGRAM, TOKEN_CHAT_ID_ADMINS
from work_in_server import WorkInServer

        

class BOT(telepot.Bot):
    def __init__(self, *args, **kwargs):
        super(BOT, self).__init__(*args, **kwargs)
        #self._answerer = telepot.helper.Answerer(self)
        self._message_with_inline_keyboard = None
        self._status_shell = False
        self._shell = WorkInServer.get_instance('shell')
        self._status_server = WorkInServer.get_instance('status_system')
        self._client_proxy = WorkInServer.get_instance('conn_client_proxy')
        self._log_client_proxy = WorkInServer.get_instance('log_client_proxy')

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.log(msg)
        if content_type == 'text':
            if self.access_in_bot_chat(msg) == True:
                if msg['text'] == '/status':
                    self.sendMessage(chat_id, self._status_server.work())
                elif msg['text'] == '/shell':
                    self.sendMessage(chat_id, "Send me a shell command") #reply_markup={'keyboard': [['Stop']]})
                    self._status_shell = True
                    self._status_shell, shell_cmd = self._shell.work()
                    self.sendMessage(chat_id, shell_cmd, disable_web_page_preview=True)
                elif msg['text'] == '/client':
                    self.sendMessage(chat_id, self._client_proxy.work())
                elif msg['text'] == '/statis_prox':
                    self.sendPhoto(chat_id, self._log_client_proxy.work())

                else:
                    if self._status_shell == True:
                        self._status_shell, shell_cmd = self._shell.work(msg['text'])
                        self.sendMessage(chat_id, shell_cmd, disable_web_page_preview=True)
                    else:
                        self.sendMessage(chat_id, 'Моя твоя не понимать')#, reply_markup={'hide_keyboard': True})


    def start_bot(self, msg):
        content_type, chat_type, chat_id, = telepot.glance(msg)
        self.sendMessage(chat_id, "Привет Хозяин")


    def access_in_bot_chat(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if str(chat_id) in TOKEN_CHAT_ID_ADMINS:
            print('Access is allowed from chat_id="{}", "{}"'.format(chat_id,msg['text']))
            return True
        else:
            print('Access is denied from chat_id="{}", "{}"'.format(chat_id, msg['text']))
            self.sendMessage(chat_id, "Я тебя не знаю. Уходи!")
            return False

    def log(self, message):
        l = "Date: {}, User:{}@{}):  {} \n".format(datetime.now(), message['chat']['id'], message['chat']['first_name'], message['text'])
        print(l)
        with open('log.txt', 'a') as f:
            f.write(l)

    def bot_handler(self, message):
        pass






































