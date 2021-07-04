from win32com.client import Dispatch
import wget
import os
import requests
from bs4 import BeautifulSoup
import re
import zipfile


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def download_new_version(version):
    try:
        os.remove(r'C:\Users\emyli\PycharmProjects\Chatbot_Project\chrome_driver\chromedriver.exe')
    except Exception as e:
        print(e)
    link = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
    filename = wget.download(link)
    # os.rename(filename, fr'C:\Users\emyli\PycharmProjects\Chatbot_Project\chrome_driver\{filename}')

    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(r'C:\Users\emyli\PycharmProjects\Chatbot_Project\chrome_driver')


def match_version(ver):
    page = requests.get('https://chromedriver.chromium.org/downloads')
    soup = BeautifulSoup(page.content, 'lxml')
    pattern = f"{ver}\.[0-9]+\.[0-9]+\.[0-9]+"
    return re.findall(pattern, str(soup))[0]


def get_driver():
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    c_ver = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    mv_ver = match_version(c_ver.split('.')[0])
    print(f'Downloading version chrome driver {mv_ver}')
    download_new_version(mv_ver)
    print('file downloaded')


if __name__ == '__main__':
    get_driver()
