import base64
import codecs as c
import socket
import os


def selector(msg):
    if msg[:len("iot graph from")] == "iot graph from":
        query = msg[len("iot graph from")+1:].strip()
        return iot_graph(query)
    elif msg[:len("iot light off for")] == "iot light off for":
        query = msg[len("iot light off for")+1:].strip()
        send_client(query, 'light off')
        return "light switched off"
    elif msg[:len("iot light on for")] == "iot light on for":
        query = msg[len("iot light on for")+1:].strip()
        send_client(query, 'light on')
        return "light switched on"


def fin2(barr, dfile):  #this returns a image
    fh = open(dfile, "wb")
    fh.write(c.decode(obj=barr, encoding='base64'))
    fh.close()


def client(host):
    port = 65001        # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            fname = "send image"
            s.sendall(fname.encode())
            data = s.recv(1024)
            l = data.decode()
            data_ = str.encode('')
            while len(data_) < int(l):
                data_ += s.recv(1024)
            file_name = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\new.png'
            fin2(barr=data_, dfile=file_name)
            #print('File received')
            s.sendall('exit'.encode())
            s.close()

    except Exception as e:
        print(e)


def send_client(host, msg):

    port = 65001  # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(msg.encode())
            s.sendall('exit'.encode())
            s.close()
    except Exception as e:
        print(e)


def iot_graph(query):
    path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\new.png'
    try:
        os.remove(path)
    except Exception as e:
        pass
    client(query)
    picture = f'<img src="new.png" alt="Iot Graph" width="65%" height="65%">'
    reply = {'display': picture, 'say': f'find below the IoT graph from {query}'}
    return reply
