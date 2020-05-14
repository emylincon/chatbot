from win32com.client import Dispatch
import wget
import os


def get_version_via_com(filename):
    parser = Dispatch("Scripting.FileSystemObject")
    try:
        version = parser.GetFileVersion(filename)
    except Exception:
        return None
    return version


def download_new_version(version):
    os.remove('chrome_driver/chromedriver.exe')
    link = f'https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip'
    filename = wget.download(link)
    os.rename(filename, f'chrome_driver/{filename}')


if __name__ == "__main__":
    paths = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    c_ver = list(filter(None, [get_version_via_com(p) for p in paths]))[0]
    print(f'Downloading version chrome driver {c_ver}')
    download_new_version(c_ver)
    print('file downloaded')
