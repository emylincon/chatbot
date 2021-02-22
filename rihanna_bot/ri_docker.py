from rihanna_bot.ri_vmware import VmWare
import paramiko
import json
import docker
import os


# docker setup https://www.youtube.com/watch?v=a5td09OWFXA
# sudo nano /lib/systemd/system/docker.service
# find ExecStart and add the following on the same line
# -H=tcp://0.0.0.0:5555
# sudo systemctl daemon-reload
# sudo service docker restart


def selector(message):
    vmware_client = VmWare()
    master = Docker(vmware_client)

    if message in master.docker_dict:
        reply = master.docker_dict[message]()
    elif message[:len('docker run')] == 'docker run':
        image = message[len('docker run') + 1:].strip()
        reply = master.run_container(image)
    elif message[:len('docker multi run')] == 'docker multi run':
        para = message[len('docker multi run') + 1:].strip().split()
        reply = master.multi_run(image=para[1], no=para[0])
    elif message[:len('docker start')] == 'docker start':
        image = message[len('docker start') + 1:].strip()
        reply = master.start_container(image)
    elif message[:len('docker stop')] == 'docker stop':
        image = message[len('docker stop') + 1:].strip()
        reply = master.stop_container(image)
    elif message[:len('docker container delete')] == 'docker container delete':
        image = message[len('docker container delete') + 1:].strip()
        reply = master.delete_container(image)
    elif message[:len('docker image delete')] == 'docker image delete':
        image = message[len('docker image delete') + 1:].strip()
        reply = master.delete_image(image)
    elif message[:len('docker pull')] == 'docker pull':
        image = message[len('docker pull') + 1:].strip()
        reply = master.delete_container(image)
    else:
        reply = "docker is offline"
        reply = {'display': reply, 'say': reply}
    vmware_client.close()
    return reply


class Docker:
    def __init__(self, vmware_client):
        self.username = os.environ['DOCKER_HOST_USERNAME']
        self.password = os.environ['DOCKER_HOST_PASSWORD']
        self.vmware_client = vmware_client
        self.ip = None
        self.port = 22
        self.docker_host_alias = 'Ubuntu.vmx'
        self.start()

    def start(self):
        self.vmware_client.change_state(name=self.docker_host_alias, state='on')
        self.ip = self.vmware_client.ip_address(name=self.docker_host_alias)['ip']

    @property
    def base_url(self):
        return f'tcp://{self.ip}:5555'

    @staticmethod
    def format_data(msg):
        out = ''
        for i in msg:
            out += i
        return out

    def send_command(self, cmd):
        c = paramiko.SSHClient()

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(self.ip, 22, self.username, self.password)

        stdin, stdout, stderr = c.exec_command(cmd)
        return self.format_data(stdout), self.format_data(stderr)

    def docker_image(self):
        do = "curl http://localhost:5555/images/json"
        data = json.loads(self.send_command(do)[0])
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

    def docker_container(self):
        do = "curl http://localhost:5555/containers/json"
        data = json.loads(self.send_command(do)[0])
        tags = ['Id', 'Names', 'Image', 'State', 'Status', 'IPAddress']
        reply = "<table id='t01'>" \
                "<tr>\
                "
        for i in tags:
            reply += f"<th><font color='blue'>{i}</font></th>"
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

    def multi_run(self, image, no):
        try:
            for i in range(int(no)):
                self.run_container(image)
            reply = f"{no} {image} has been deployed on server"
            return {'display': reply, 'say': reply}
        except Exception as e:
            reply = f"Error in multi_run: {e}"
            return {'display': reply, 'say': reply}

    def run_container(self, image):
        do = f"docker run -ti --detach {image}"
        data, err = self.send_command(do)
        if len(data) == 0 and len(err) > 0:
            reply = "Error occurred could not find image"
            return {'display': reply, 'say': reply}
        else:
            reply = "container is running"
            return {'display': reply, 'say': reply}

    def start_container(self, con_name):
        do = f"docker start {con_name}"
        data, err = self.send_command(do)
        if len(data) == 0 and len(err) > 0:
            reply = "Error occurred could not find image"
            return {'display': reply, 'say': reply}
        else:
            reply = "container is running"
            return {'display': reply, 'say': reply}

    def _stop_container(self, con_name):
        do = f"docker stop {con_name}"
        data, err = self.send_command(do)
        if len(data) == 0 and len(err) > 0:
            reply = "Error occurred could not find image"
            return {'display': reply, 'say': reply}
        else:
            reply = "container is running"
            return {'display': reply, 'say': reply}

    def delete_container(self, con_name):
        do = f"docker container rm {con_name}"
        data, err = self.send_command(do)
        if len(data) == 0 and len(err) > 0:
            reply = "Error occurred could not find image"
            return {'display': reply, 'say': reply}
        else:
            reply = f"{con_name} container has been deleted"
            return {'display': reply, 'say': reply}

    def delete_image(self, image):
        do = f"docker image rm {image}"
        data, err = self.send_command(do)
        if len(data) == 0 and len(err) > 0:
            reply = "Error occurred could not find image"
            return {'display': reply, 'say': reply}
        else:
            reply = f"{image} Image has been deleted"
            return {'display': reply, 'say': reply}

    def stop_container(self, con_name):
        client = docker.DockerClient(base_url=self.base_url)
        try:
            con = client.containers.get(con_name)
            con.stop()
            reply = f"{con_name} has been stopped"
            return {'display': reply, 'say': reply}
        except Exception as e:
            reply = f'stop container error: {e}'
            return {'display': reply, 'say': reply}

    def prune_containers(self):
        client = docker.DockerClient(base_url=self.base_url)
        client.containers.prune()
        reply = "All stopped containers have been deleted"
        return {'display': reply, 'say': reply}

    def docker_container_list(self):
        client = docker.DockerClient(base_url=self.base_url)
        data = client.containers.list(all)
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
        client.close()
        return reply_

    def container_network(self):
        client = docker.DockerClient(base_url=self.base_url)
        data = client.containers.list()
        tags = ['Id', 'Names', 'Image', 'IPAddress', 'MacAddress', 'Gateway']
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
            reply += f"<td>{container.attrs['NetworkSettings']['IPAddress']}</td>"
            reply += f"<td>{container.attrs['NetworkSettings']['MacAddress']}</td>"
            reply += f"<td>{container.attrs['NetworkSettings']['Gateway']}</td>"
            reply += f"<tr>"
        reply += "</table>"
        reply_ = {'display': reply, 'say': 'Find below the Network configurations of the running containers'}
        client.close()
        return reply_

    def container_utils(self):
        client = docker.DockerClient(base_url=self.base_url)
        data = client.containers.list()
        tags = ['Id', 'Names', 'Image', 'CPU Usage', 'Memory Usage']
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
            reply += f"<td>{container.attrs['HostConfig']['CpuPercent']}</td>"
            reply += f"<td>{container.attrs['HostConfig']['Memory']}</td>"
            reply += f"<tr>"
        reply += "</table>"
        reply_ = {'display': reply, 'say': 'Find below the Utilization of the running containers'}
        client.close()
        return reply_

    def run_container_cmd(self, image, cmd):
        client = docker.DockerClient(base_url=self.base_url)
        con = client.containers.run('ubuntu', command='it', detach=True)
        # not completed

    def docker_pull(self, image):
        client = docker.DockerClient(base_url=self.base_url)
        try:
            client.images.pull(image)
            client.close()
            reply = f"{image} created"
            return {'display': reply, 'say': reply}
        except Exception:
            client.close()
            reply = f"could not find {image}"
            return {'display': reply, 'say': reply}

    @property
    def docker_dict(self):
        return {'docker image list': self.docker_image, 'docker container list': self.docker_container_list,
                'docker container network': self.container_network,
                'docker container utilization': self.container_utils,
                'docker prune': self.prune_containers}

# docker_dict = {'docker image list': docker_image, 'docker container list': docker_container_list,
#                'docker container network': container_network, 'docker container utilization': container_utils,
#                'docker prune': prune_containers}

# a = selector('docker container list')
# print(a)