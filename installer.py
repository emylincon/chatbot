import os
import subprocess as sp
x = open('packages.txt','r')
y = x.readlines()
for i in y:
    if i != '':
        cmd = f'pip3 install {i}'
        print(f'installing {i}')
        os.system(cmd)

import nltk
nltk.download('all')
nltk.download('punkt')
nltk.download('popular')
os.system('apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable')
os.system('apt --fix-broken install')
os.system('wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb')
os.system('dpkg -i google-chrome-stable_current_amd64.deb')
get_version = 'google-chrome-stable --version'
cmd = [get_version]
version_raw = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
version = version_raw.split()[-1]
link_chrome_driver = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_linux64.zip'
os.system(f'wget {link_chrome_driver}')
os.system('unzip chromedriver_linux64.zip')