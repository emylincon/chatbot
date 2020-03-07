import base64
import codecs as c
import socket
import os
import time


ip = '10.1.2.117'


def selector(msg):
    if msg[:len("iot graph from")] == "iot graph from":
        query = msg[len("iot graph from")+1:].strip()
        if query[0].isdigit():
            return iot_graph(query)
        else:
            return iot_graph(ip)
    elif msg[:len("iot light off for")] == "iot light off for":
        host_ip = msg[len("iot light off for")+1:].strip()
        if host_ip[0].isdigit():
            send_client(host_ip, 'light off')
        else:
            send_client(ip, 'light off')
        reply = "light switched off"
        return {'display': reply, 'say': reply}
    elif msg[:len("iot light on for")] == "iot light on for":
        host_ip = msg[len("iot light on for")+1:].strip()
        if host_ip[0].isdigit():
            send_client(host_ip, 'light on')
        else:
            send_client(ip, 'light on')
        #send_client(host_ip, 'light on')
        reply = "light switched on"
        return {'display': reply, 'say': reply}
    elif msg[:len("iot temperature for")] == "iot temperature for":
        host_ip = msg[len("iot temperature for") + 1:].strip()
        if host_ip[0].isdigit():
            data = send_recv_client(host_ip, "last temp")
        else:
            data = send_recv_client(ip, "last temp")
        reply = "last recorded temperature is "+ data+ ' Celsius' if data[0].isdigit() else data
        return {'display': reply, 'say': reply}
    elif msg[:len("iot cpu for")] == "iot cpu for":
        host_ip = msg[len("iot cpu for") + 1:].strip()
        if host_ip[0].isdigit():
            data = send_recv_client(host_ip, "cpu util")
        else:
            data = send_recv_client(ip, "cpu util")
        reply = "last cpu utilization is ", data if data[0].isdigit() else data
        return {'display': reply, 'say': reply}
    elif msg[:len("iot memory for")] == "iot memory for":
        host_ip = msg[len("iot memory for") + 1:].strip()
        if host_ip[0].isdigit():
            data = send_recv_client(host_ip, "mem util")
        else:
            data = send_recv_client(ip, "mem util")
        reply = "last memory utilization is ", data if data[0].isdigit() else data
        return {'display': reply, 'say': reply}
    elif msg[:len("iot humidity for")] == "iot humidity for":
        host_ip = msg[len("iot humidity for") + 1:].strip()
        if host_ip[0].isdigit():
            data = send_recv_client(host_ip, "last hum")
        else:
            data = send_recv_client(ip, "last hum")
        reply = "Humidity Level is at "+ data+" Percent" if data[0].isdigit() else data
        return {'display': reply, 'say': reply}
    else:
        reply = "Rihanna is busy at the moment"
        return {'display': reply, 'say': reply}


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
            data_length = data.decode()
            if len(data_length) > 0:
                data_ = str.encode('')
                while len(data_) < int(data_length):
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
        reply = "server not responding"
        return {'display': reply, 'say': reply}


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
