import os

def selector(msg):
    if msg == 'deploy a webserver':
        pass
    pass


class Control:
    def __init__(self):
        self.containers = []
        self.name = 1

    def webserver(self, name=None):
        if name:
            os.system(f'docker run -idt --name {name} -p 8080:80 nginx')
        else:
            os.system(f'docker run -idt --name con{self.name} -p 8080:80 nginx')
            self.name += 1