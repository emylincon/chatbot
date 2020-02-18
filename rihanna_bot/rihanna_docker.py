import paramiko
import config as cf
import json
import ast


def selector(message):
    if message == 'docker container list':
        return docker_container()
    elif message == 'docker image list':
        return docker_image()
    else:
        return "docker is offline"


def format_data(msg):
    out = ''
    for i in msg:
        out += i
    return out


def send_command(cmd):
    c = paramiko.SSHClient()

    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c.connect(cf.docker_host['ip'], 22, cf.docker_host['un'], cf.docker_host['pw'])
    # cmd = "curl http://localhost:5555/images/json"

    stdin, stdout, stderr = c.exec_command(cmd)
    return format_data(stdout), format_data(stderr)


def docker_image():
    do = "curl http://localhost:5555/images/json"
    data = json.loads(send_command(do)[0])
    reply = ''
    reply += "<table id='t01'>\
                    <tr>\
                        <th>Images</th>\
                    </tr>\
                    "
    for i in data:
        reply += f"<tr>\
                        <td>{i['RepoTags'][0]}</td>\
                   </tr>"

    reply += "</table>"
    reply_ = {'display': reply, 'say': 'Find below the list of images'}
    return reply_


def docker_container():
    do = "curl http://localhost:5555/containers/json"
    data = json.loads(send_command(do)[0])
    tags = ['Id', 'Names', 'Image', 'State', 'Status', 'IPAddress']
    reply = "<table id='t01'>"\
            "<tr>\
            "
    for i in tags:
        f"<th><font color='blue'>{i}</font></th>"
    reply += "</tr>"

    for container in data:
        reply += f"<tr>"
        reply += f"<td>{container['Id'][:10]}</td>"
        for i in tags[1:-1]:
            reply += f"<td>{container[i]}</td>"
        reply += f"<td>{container['NetworkSettings']['Networks']['bridge']['IPAddress']}</td>"
        reply += f"<tr>"
    reply += "</table>"
    reply_ = {'display': reply, 'say': 'Find below the list of containers'}
    return reply_


#docker_container()

