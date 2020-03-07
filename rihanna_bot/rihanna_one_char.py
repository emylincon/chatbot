

def _number(x):
    reply = x + 1
    return {'display': reply, 'say': reply}


def _char(ch):
    if ch == 'z':
        reply = 'z'
        return {'display': reply, 'say': reply}
    else:
        reply = chr(ord(ch)+1)
        return {'display': reply, 'say': reply}


def main(msg):
    if msg.isdigit():
        return _number(int(msg))
    else:
        return _char(msg)
