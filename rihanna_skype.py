from skpy import Skype
import config as con
import datetime as dt

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


def _skype(message):
    if message.strip()[:4] == 'chat':
        new_msg = message.strip()[5:].split()
        _name = new_msg[0]
        _msg = ' '.join(new_msg[1:])
        return send_message(_name, _msg)


def show_picture(name):
    if name.lower() in con.friends:
        p_id = con.friends[name.lower()]
        picture = f'<img src="https://avatar.skype.com/v1/avatars/{p_id}/public">'
        return picture
    else:
        return f"Sorry I do not know {name}"


def birthday(name):
    try:
        if name.lower() in con.friends:
            p_id = con.friends[name.lower()]
            _birth = contacts[p_id].birthday
            now = dt.date.today().year

            return f"{name} was born on {str(_birth)}, so {now - _birth.year} years old"
        else:
            return f"Sorry I do not know {name}"
    except AttributeError:
        return "Sorry I do not know"


def send_message(name, message):
    if name.lower() in con.friends:
        chat = contacts[con.friends[name.lower()]].chat
        sk.chats[chat.id].sendMsg(message)
        return f"Message sent to {name}"
    else:
        return f"{name} is not in your friend list"


# docs for skype
# https://github.com/Terrance/SkPy.docs
# https://pypi.org/project/SkPy/
print(birthday('jess'))

