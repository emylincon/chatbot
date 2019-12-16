import datetime
import time


def rihanna_time():
    _time = str(datetime.datetime.now()).split()[1].split('.')[0]
    return f'The Time is {_time}'


def rihanna_date():
    return time.ctime()
