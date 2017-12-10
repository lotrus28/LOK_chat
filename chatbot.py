#this is a sample chatbot that conducts very simple operation with messages
#this operation was meant to be replaced by text analysis
#the bot should recieve messages from operator-client chat and respond to operator-bot chat (giving advise)

#importing libraries to recieve, process and send messages in Telegram
import json 
import requests
import time
import urllib
import sqlite3
#library for sample operation
from PyDictionary import PyDictionary

#api token
TOKEN = "api token of bot (removed)"
#url template
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#download information from url
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

#obtain information in json-format
def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

#list messages which are sent to the bot (get only recent messages according to offset value)
#save resources due to timeout parameter
def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

#get the latest update ID (to reply all meassages including duplicates)
def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

#obtain chat id and latest messages in the chat
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#sending message to the selected chat
def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
#    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, #id of operator-bot chat)
#    print(chat_id)
    get_url(url)
    
#reply to all recieved message
def echo_all(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            #performing sample operation with text (in this example the bot sends antonyms to english words)
            dictionary = PyDictionary()
            text = str(dictionary.antonym(text)[1])
            send_message(text, chat)
#            print(text)
        except Exception as e:
            print(e)
                                                        
#final replying function
def main():
    db.setup()
    last_update_id = None
    while True:
#        print("getting updates")
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            echo_all(updates)
        time.sleep(0.5)

#activation
if __name__ == '__main__':
    main()