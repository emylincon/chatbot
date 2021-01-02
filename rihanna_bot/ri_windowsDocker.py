import os
import docker
import zipfile
import random
from jinja2 import Environment, FileSystemLoader
import requests

''':key
url for doc = https://docker-py.readthedocs.io/en/stable/containers.html
'''


def selector(msg):
    if msg == 'deploy a webserver':
        return docker_master.webserver1()
    elif msg == 'deploy webserver template for editing':
        return docker_master.container_run()
    elif msg == 'show container list':
        return docker_master.docker_container_list()
    elif msg[:len('stop container')] == 'stop container':
        con = msg[len('stop container')+1:].strip()
        return docker_master.stop_container(con_name=con)
    elif msg == 'prune containers':
        return docker_master.prune_containers()
    else:
        return 'Unknown Request'


class BuildWebsite:
    def __init__(self):
        file_loader = FileSystemLoader(r'C:\Users\emyli\PycharmProjects\Chatbot_Project\templates')
        self.env = Environment(loader=file_loader)
        self.output_path = r'C:\Users\emyli\PycharmProjects\Chatbot_Project\template_output'
        self.github = 'https://api.github.com/users' # 'https://api.github.com/users/emylincon' https://api.github.com/users/emylincon/repos
        self.point = 0
        self.template_path = r'E:\Vscode Project'

    @staticmethod
    def get_name():
        return random.randrange(1000, 9999)

    def get_user(self, username):
        url_profile = f'{self.github}/{username}'
        profile = requests.get(url_profile).json()
        url_repos = f'{self.github}/{username}/repos'
        repo = requests.get(url_repos).json()
        return profile, repo

    def provision_resources(self, name, template):
        directory = f'{self.template_path}/{name}'
        os.mkdir(directory)
        filename = f'{self.template_path}/{template}'
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(directory)
        return directory

    def create(self, username):
        template = self.env.get_template(f'temp{self.point+1}.html')
        temp = f'temp{self.point+1}.zip'
        name = f'web{self.get_name()}'
        self.point ^= 1
        web_path = self.provision_resources(name=name, template=temp)
        profile, repo = self.get_user(username=username)
        template.stream(profile=profile, repo=repo[-6:]).dump(fr'{web_path}/index.html')
        return web_path


class Control:
    def __init__(self):
        self.containers = []
        self.client = docker.from_env()
        self.base = r'E:\Vscode Project'
        self.template = r'E:\Vscode Project\templates'
        self.web_builder = BuildWebsite()

    def get_port(self, name):
        con = self.client.containers.get(name)
        port = list(con.__dict__['attrs']['NetworkSettings']['Ports'].values())[0][0]['HostPort']
        return port

    def webserver(self, name=None):
        if name:
            os.system(f'docker run -idt --name {name} -P nginx')
        else:
            os.system(f'docker run -idt --name con{self.name} -P nginx')
        port = self.get_port(name)
        reply = f'Your webserver have been deployed on port {port}'
        return {'display': reply + f'<br> <a href="http://localhost:{port}">access webserver</a>', 'say': reply}

    @property
    def name(self):
        return random.randrange(100000)
    
    def webserver1(self, name=None):
        if name:
            self.client.containers.run(name=name, image='nginx', ports={'80/tcp': None}, detach=True)
        else:
            name = f'con{self.name}'
            self.client.containers.run(name=name, image='nginx', ports={'80/tcp': None}, detach=True)
        port = self.get_port(name)
        reply = f'Your webserver have been deployed on port {port}'
        return {'display': reply + f'<br> <a href="http://localhost:{port}">access webserver</a>', 'say': reply}

    def docker_container_list(self):
        data = self.client.containers.list(all)
        tags = ['Id', 'Names', 'Image', 'Status']
        reply = "<table id='t01'>" \
                "<tr>\
                "
        for i in tags:
            reply += f"<th><font color='blue'>{i}</font></th>"
        reply += "</tr>"
        for container in data:
            reply += f"<tr>"
            reply += f"<td>{container.attrs['Config']['Hostname']}</td>"
            reply += f"<td>{container.attrs['Name'][1:]}</td>"
            reply += f"<td>{container.attrs['Config']['Image']}</td>"
            status = container.attrs['State']['Status']
            if status == 'running':
                reply += f"<td><font color='green'>{status}</font></td>"
            elif status == 'created':
                reply += f"<td><font color='yellow'>{status}</font></td>"
            else:
                reply += f"<td><font color='red'>{status}</font></td>"
            reply += f"<tr>"
        reply += "</table>"
        reply_ = {'display': reply, 'say': 'Find below the list of containers'}
        return reply_

    def stop_container(self, con_name):
        try:
            con = self.client.containers.get(con_name)
            con.stop()
            reply = f"{con_name} has been stopped"
            return {'display': reply, 'say': reply}
        except Exception as e:
            reply = f'stop container error: {e}'
            return {'display': reply, 'say': reply}

    def prune_containers(self):
        self.client.containers.prune()
        reply = "All stopped containers have been deleted"
        return {'display': reply, 'say': reply}

    def provision_resources(self, name):
        directory = f'{self.base}/{name}'
        os.mkdir(directory)
        filename = f'{self.template}/{random.choice(os.listdir(self.template))}'
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(directory)
        return directory

    def container_run(self, image='nginx', detach=True):
        name = f'con{self.name}'
        volume = self.provision_resources(name)
        self.client.containers.run(name=name, image=image, ports={'80/tcp': None}, detach=detach,
                                   volumes={volume: {'bind': '/usr/share/nginx/html/', 'mode': 'rw'}})
        os.system(f'code -n "{volume}"')
        port = self.get_port(name)
        reply = f'Your {image} server have been deployed on port {port}. Opening code editor'
        return {'display': reply+f'<br> <a href="http://localhost:{port}">access webserver</a>', 'say': reply}

    def container_web(self, username, image='nginx', detach=True):
        name = f'con{self.name}'
        volume = self.web_builder.create(username=username)
        self.client.containers.run(name=name, image=image, ports={'80/tcp': None},
                                   detach=detach,
                                   volumes={volume: dict(bind='/usr/share/nginx/html/', mode='rw')})
        os.system(f'code -n "{volume}"')
        port = self.get_port(name)
        reply = f'Web portfolio for {username} has been deployed on port {port}. Opening code editor'
        return {'display': reply+f'<br> <a href="http://localhost:{port}">access portfolio</a>', 'say': reply}


docker_master = Control()
# docker_master.container_run()