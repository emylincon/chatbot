# This script is using Python3
import urllib.request
import urllib.parse
import config
import json


def selector(message):
    if message[:len('nhs review on')] == 'nhs review on':
        msg = message[len('nhs review on')+1:].strip()
        return HealthData(msg).display_all()
    elif message[:len('nhs prevention for')] == 'nhs prevention for':
        msg = message[len('nhs prevention for')+1:].strip()
        return HealthData(msg, "prevention").content_attrs()
    elif message[:len('nhs overview for')] == 'nhs overview for':
        msg = message[len('nhs overview for')+1:].strip()
        return HealthData(msg, "overview").content_attrs()
    elif message[:len('nhs symptoms for')] == 'nhs symptoms for':
        msg = message[len('nhs symptoms for') + 1:].strip()
        return HealthData(msg, "symptoms").content_attrs()
    elif message[:len('nhs treatments overview for')] == 'nhs treatments overview for':
        msg = message[len('nhs treatments overview for') + 1:].strip()
        return HealthData(msg, "treatments_overview").content_attrs()
    elif message[:len('nhs self care advice for')] == 'nhs self care advice for':
        msg = message[len('nhs self care advice for') + 1:].strip()
        return HealthData(msg, "self_care").content_attrs()
    elif message[:len('nhs other treatments for')] == 'nhs other treatments for':
        msg = message[len('nhs other treatments for') + 1:].strip()
        return HealthData(msg, "other_treatments").content_attrs()
    elif message[:len('nhs causes for')] == 'nhs causes for':
        msg = message[len('nhs causes for') + 1:].strip()
        return HealthData(msg, "causes").content_attrs()
    else:
        return "NHS server cannot process that request at the moment"


class HealthData:
    def __init__(self, search, name=None):
        self.request_headers = {
            "subscription-key": config.nhs_Key,
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        self.search = search
        self.baseUrl = "https://api.nhs.uk/conditions"
        self.name = name

    def display_all(self):
        pageURL = f"{self.baseUrl}/{self.search}"
        try:
            request = urllib.request.Request(pageURL, headers=self.request_headers)
            contents = json.loads(urllib.request.urlopen(request).read())
            reply = f"<h1><font color='blue'>NHS REVIEW ON {self.search.upper()}</font></h1>"
            for data_dict in contents["hasPart"]:
                reply += f"<h3>{data_dict['name'].capitalize().replace('_', ' ')}</h3>"
                text = data_dict["text"]
                if text == "":
                    text = data_dict["description"]
                reply += f"{text.replace(';', '').replace('api', 'www')}"
                reply += f'<a href="{data_dict["url"].replace("api", "www")}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed a review on {self.search}. this information is provided by NHS'}
            return reply_

        except Exception:
            return f"cannot find result for {self.search}"

    def _get_parts(self, name):
        try:
            pageURL = f"{self.baseUrl}/{self.search}"
            request = urllib.request.Request(pageURL, headers=self.request_headers)
            contents = json.loads(urllib.request.urlopen(request).read())
            data_attrs = {}
            for data_dict in contents['hasPart']:
                text = data_dict["text"]
                if text == "":
                    text = data_dict["description"]
                data_attrs[data_dict["name"]] = text
            if name in data_attrs:
                return data_attrs[name]
            else:
                return 0
        except Exception:
            return 0

    def causes(self):
        name = "causes"
        data = self._get_parts(name)
        if data != 0:
            reply = f"<h2><font color='blue'>{name.capitalize()} of {self.search.upper()}</font></h2>"
            reply += f"<p>{data[name]}</p>"
            reply += f'<a href="{self.baseUrl}/{self.search}/#{name}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed {name} of {self.search}. this information is provided by NHS'}
            return reply_
        else:
            return f"cannot find result for {self.search}"

    def symptoms(self):
        name = "symptoms"
        data = self._get_parts(name)
        if data != 0:
            reply = f"<h2><font color='blue'>{name.capitalize()} of {self.search.upper()}</font></h2>"
            reply += f"<p>{data[name]}</p>"
            reply += f'<a href="{self.baseUrl}/{self.search}/#{name}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed {name} of {self.search}. this information is provided by NHS'}
            return reply_
        else:
            return f"cannot find result for {self.search}"

    def treatments(self):
        name = "treatments_overview"
        data = self._get_parts(name)
        if data != 0:
            reply = f"<h2><font color='blue'>{name.capitalize().replace('_', ' ')} of {self.search.upper()}</font></h2>"
            reply += f"<p>{data[name]}</p>"
            reply += f'<a href="{self.baseUrl}/{self.search}/#{name}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed {name.capitalize().replace("_", " ")} of {self.search}. '
                             f'this information is provided by NHS'}
            return reply_
        else:
            return f"cannot find result for {self.search}"

    def self_care(self):
        name = "treatments_overview"
        data = self._get_parts(name)
        if data != 0:
            reply = f"<h2><font color='blue'>{name.capitalize().replace('_', ' ')} of {self.search.upper()}</font></h2>"
            reply += f"<p>{data}</p>"
            reply += f'<a href="{self.baseUrl}/{self.search}/#{name}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed {name.capitalize().replace("_", " ")} of {self.search}. '
                             f'this information is provided by NHS'}
            return reply_
        else:
            return f"cannot find result for {self.search}"

    def content_attrs(self):
        data = self._get_parts(self.name)
        if data != 0:
            reply = f"<h2><font color='blue'>{self.name.capitalize().replace('_', ' ')} of {self.search.upper()}</font></h2>"
            reply += f"{data.replace(';', '')}"
            reply += f'<a href="{self.baseUrl}/{self.search}/#{self.name}" target="_blank">Read More</a>'
            reply_ = {'display': reply,
                      'say': f'Find displayed {self.name.capitalize().replace("_", " ")} of {self.search}. '
                             f'this information is provided by NHS'}
            return reply_
        else:
            return f"cannot find result for {self.search}"


