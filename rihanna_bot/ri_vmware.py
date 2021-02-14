import requests
import json
import os
import subprocess as sp
from threading import Thread
import socket

# https://www.youtube.com/watch?v=AsOm56jGNCE&ab_channel=ThePacketThrower
# openssl req -x509 -sha256 -nodes -newkey rsa:4096 -keyout vmware-key.pem -out vmware-crt.pem -days 365


class VmWare:
    def __init__(self):
        self.url = "https://127.0.0.1:8697/api/vms"
        self.start_path = r'C:\Program Files (x86)\VMware\VMware Workstation\certs'
        self.rest_app = r'C:\Program Files (x86)\VMware\VMware Workstation\vmrest.exe'
        self.server = 'vmrest.exe'
        self.payload = {}
        self.headers = {
            'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
            'Content-Type': 'application/vnd.vmware.vmw.rest-v1+json',
        }
        self.username = os.environ['VMWARE_USERNAME']
        self.password = os.environ['VMWARE_PASSWORD']
        self.server_process = None
        self.port = 8697
        self.start()

    def server_is_running(self):
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        location = ("127.0.0.1", self.port)
        result_of_check = a_socket.connect_ex(location)
        a_socket.close()
        if result_of_check == 0:
            print('PORT IS OPEN')
            return True   # means port is open
        else:
            print('PORT IS CLOSE')
            return False

    def start_server(self):
        sp.run(f'"{self.rest_app}" -c vmware-crt.pem -k vmware-key.pem', shell=True, capture_output=True, text=True)

    def start(self):
        os.chdir(self.start_path)
        if not self.server_is_running():
            print('STARTING SERVER')
            self.server_process = Thread(target=self.start_server)
            self.server_process.start()
    
    def close(self):
        os.system(f"taskkill /f /im  {self.server}")

    def get_vms_all(self):
        response = requests.request("GET", self.url, headers=self.headers, auth=(self.username, self.password),
                                    data=self.payload, verify=False)
        return json.loads(response.content)

    def get_vm_id(self, name):
        vms = self.get_vms_all()
        for vm_dict in vms:
            if vm_dict['path'].split('\\')[-1] == name:
                return vm_dict['id']
        return None

    def change_state(self, state, name):
        """:key
        state = on, off, suspended
        valid operations = VM power operation: on, off, shutdown, suspend, pause, unpause
        """
        states = {'on': "poweredOn", 'off': "poweredOff"}
        vm_id = self.get_vm_id(name)
        cur_state = self.power_state(name, vm_id=vm_id)
        if cur_state:
            if cur_state['power_state'] != states[state.lower()]:
                response = requests.request("PUT", f'{self.url}/{vm_id}/power', headers=self.headers,
                                            auth=(self.username, self.password),
                                            data=state, verify=False)
                return json.loads(response.content)
        return {'msg': f'state = {states[state]}'}

    def power_state(self, name, vm_id=None):
        """:key
        returns {"power_state": "poweredOff"} or {"power_state": "poweredOn"} or None
        """

        def get_state(vm_id):
            url = f'{self.url}/{vm_id}/power'
            response = requests.request("GET", url, headers=self.headers, auth=(self.username, self.password),
                                        data=self.payload, verify=False)
            return json.loads(response.content)

        if vm_id:
            return get_state(vm_id)
        else:
            vm_id = self.get_vm_id(name)
            if vm_id:
                return get_state(vm_id)
        return None

    def ip_address(self, name, vm_id=None):
        def get_ip(vm_id):
            url = f'{self.url}/{vm_id}/ip'
            response = requests.request("GET", url, headers=self.headers, auth=(self.username, self.password),
                                        data=self.payload, verify=False)
            return json.loads(response.content)

        if vm_id:
            return get_ip(vm_id)
        else:
            vm_id = self.get_vm_id(name)
            if vm_id:
                return get_ip(vm_id)
        return None

# a = VmWare().get_vm_id('Ubuntu.vmx')
# print('id ->', a)

# obj = VmWare()
# a = obj.change_state(name='Ubuntu.vmx', state='off')
# print('state ->', a)
# obj.close()

# obj = VmWare()
# a = obj.ip_address(name='Ubuntu.vmx')
# print('ip ->', a)
# obj.close()

# r = requests.put('https://127.0.0.1:8697/api/vms/7A7K84LC1BARGPQFV3S3PHV3CLRVB2TB/power', headers=headers,
#                  verify=False, data='off')
#
# print(json.loads(r.content))
