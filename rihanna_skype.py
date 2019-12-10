from skpy import Skype
import config as con

sk = Skype(con.skype_name, con.skype_password)
contacts = sk.contacts

'''
for i in c_ids:
    name = contacts.contact(i).name.first
    #print(name)
    if name:
        #print(name)
        friends[name.lower()] = i
'''


def send_message(name, message):
    if name.lower() in con.friends:
        chat = contacts[con.friends[name.lower()]].chat
        sk.chats[chat.id].sendMsg(message)
        return "Message sent"
    else:
        return f"{name} is not in your friend list"


# docs for skype
# https://github.com/Terrance/SkPy.docs
# https://pypi.org/project/SkPy/


