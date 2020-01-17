import base64
import codecs as c
import socket
import os
import time


def selector(msg):
    if msg[:len("iot graph from")] == "iot graph from":
        query = msg[len("iot graph from")+1:].strip()
        return iot_graph(query)
    elif msg[:len("iot light off for")] == "iot light off for":
        host_ip = msg[len("iot light off for")+1:].strip()
        send_client(host_ip, 'light off')
        return "light switched off"
    elif msg[:len("iot light on for")] == "iot light on for":
        host_ip = msg[len("iot light on for")+1:].strip()
        send_client(host_ip, 'light on')
        return "light switched on"
    elif msg[:len("iot temperature for")] == "iot temperature for":
        host_ip = msg[len("iot temperature for") + 1:].strip()
        data = send_recv_client(host_ip, "last temp")
        return "last temp is ", data if data[0].isdigit() else data
    elif msg[:len("iot cpu for")] == "iot cpu for":
        host_ip = msg[len("iot cpu for") + 1:].strip()
        data = send_recv_client(host_ip, "cpu util")
        return "last cpu utilization is ", data if data[0].isdigit() else data
    elif msg[:len("iot memory for")] == "iot memory for":
        host_ip = msg[len("iot memory for") + 1:].strip()
        data = send_recv_client(host_ip, "mem util")
        return "last memory utilization is ", data if data[0].isdigit() else data
    else:
        return "Rihanna is busy at the moment"


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
        print('Error from client: ', e)


def send_client(host, msg):

    port = 65001  # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(msg.encode())
            time.sleep(1)
            s.sendall('exit'.encode())
            s.close()
    except Exception as e:
        print('Error from send_client: ', e)


def send_recv_client(host, msg):

    port = 65001  # The port used by the server

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall(msg.encode())
            time.sleep(1)
            data = s.recv(1024)
            reply = data.decode()
            s.sendall('exit'.encode())
            s.close()
            return reply
    except Exception as e:
        print('Error from send_client: ', e)
        return "server not responding"


def iot_graph(query):
    path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\new.png'
    try:
        os.remove(path)
    except Exception as e:
        pass
    client(query)
    picture = f'<img src="new.png?{time.time()}" alt="Iot Graph" width="65%" height="65%">'
    reply = {'display': picture, 'say': f'find below the IoT graph from {query}'}
    return reply
