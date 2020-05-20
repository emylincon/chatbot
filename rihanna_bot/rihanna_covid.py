import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
import sys, traceback
import os
from rihanna_bot.download_chrome_driver import get_driver


def selector(query):
    if query[:len('covid cases for ')] == 'covid cases for ':
        msg = query[len('covid cases for '):]
        return Report().display_place(msg)
    elif query == 'covid cases':
        return Report().display_all()


class Report:
    def __init__(self):
        self.url = 'https://www.worldometers.info/coronavirus/'
        self.heading = ''
        self.raw_table = ''
        self.data = self.get_data()

    def get_data(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            try:
                chrome_p = os.listdir('chrome_driver/')[0]
                chrome_path = f'chrome_driver/{chrome_p}'
            except:
                chrome_p = os.listdir('../chrome_driver/')[0]
                chrome_path = f'../chrome_driver/{chrome_p}'
            driver = webdriver.Chrome(chrome_path, options=options)
            driver.get(self.url)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            self.raw_table = table = soup.find("table", {"id": "main_table_countries_today"})
            heads = table.find('thead').find_all('th')
            heading = []
            for th in heads:
                head = th.get_text().replace('<br>', ' ').replace('\n', '').split(',')[0]
                if head == 'Tot\xa0Cases/1M pop':
                    head = 'TotalCases/1M pop'
                heading.append(head)

            self.heading = heading

            tbody = table.find('tbody').find_all('tr')
            data = {}
            for tr in tbody:
                row = tr.find_all('td')
                key = row[0].get_text().replace('\n', '').lower()
                data[key] = {}
                for i in range(len(heading[1:])):
                    data[key][heading[i+1]] = row[i+1].get_text()

            return data
        except Exception as e:
            if {'ChromeDriver', 'version'} - set(str(e).split()) == set():
                get_driver()
                return self.get_data()
            else:
                traceback.print_exc()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                print(exc_value)
                return 'Bug detected'

    def display_all(self):
        display = "<table id='t01'><tr>"
        for head in self.heading:
            if '/' in head:
                h = head.split('/')
                head = f"{h[0]}<br>({h[1]})"
            display += f"<th><p style='font-size:13px; color:#5985E9; font-family:verdana;'>{head}</p></th>"
        display += "</tr>"
        for country in self.data:
            display += '<tr>'
            display += f"<td><p style='font-size:10px; color:#3C6BD3; font-family:verdana;'>{country.title()}</p></td>"
            for value in self.data[country].values():
                if value == '':
                    display += f"<td><p style='font-size:10px; color:#3C6BD3; font-family:verdana;'>-</p></td>"
                else:
                    display += f"<td><p style='font-size:10px; color:#3C6BD3; font-family:verdana;'>{value}</p></td>"
            display += '</tr>'
        display += '</table>'
        say = f'Find displayed the available data on COVID19 updated on {str(datetime.datetime.now()).split()[0]}'
        return {'display': display, 'say': say}

    def display_place(self, place):
        for i in self.data:
            if place.lower() == self.data[i]['Country'].lower():
                display = "<table id='t01'><tr>"
                for value in self.data[i]:
                    display += f"""<tr>
                                  <td style='font-size:16px;'><b>{value}</b></td>
                                  <td>{self.data[i][value]}</td>
                                  </tr>"""
                display += '</table>'
                say = f"find covid19 details for {place} updated on {str(datetime.datetime.now()).split()[0]}"
                width = 450
                reply = f'''<div style="width: {width}px;">
                        <p style="text-align: center;"><b>{self.data[i]['Country']}</b></p>
                        <table style="width: {width}px; color: grey;">
                        <tr>
                            <td><b>Total Cases</b></td>
                            <td style="text-align:left;"><b>{self.data[i]['TotalCases']}</b></td>
                        </tr>
                        </table>
                        
                        <div style="width: 100%; border-bottom: 1px solid grey;"></div>
                        <table style="width: {width}px;">
                        <tr>
                            <td><div style="border-radius: 50%; background-color:rgb(179, 255, 0); height: 10px; width: 10px;"></div></td>
                            <td>Active Cases</td>
                            <td style="text-align:left;">{self.data[i]['ActiveCases']}</td>
                        </tr>
                        <tr>
                            <td><div style="border-radius: 50%; background-color: green; height: 10px; width: 10px;"></div></td>
                            <td>Recovered Cases</td>
                            <td style="text-align:left;">{self.data[i]['TotalRecovered']}</td>
                        </tr>
                        <tr>
                            <td><div style="border-radius: 50%; background-color:red; height: 10px; width: 10px;"></div></td>
                            <td>Deaths</td>
                            <td ><span style="text-align:left;">{self.data[i]['TotalDeaths']}</span></td>
                        </tr>
                        </table>
                    </div>
                    <br>
                    <button type="button" class="collapsible">More</button>
                    <div class="content">{display}</div>'''
                script = '<script>\
                                        var coll = document.getElementsByClassName("collapsible");\
                                        var i;\
                                        for (i = 0; i < coll.length; i++) {\
                                          coll[i].addEventListener("click", function() {\
                                            this.classList.toggle("active");\
                                            var content = this.nextElementSibling;\
                                            if (content.style.maxHeight){\
                                              content.style.maxHeight = null;\
                                            } else {\
                                              content.style.maxHeight = content.scrollHeight + "px";\
                                            } \
                                          });\
                                        }\
                                        </script>'
                return {'display': reply+script, 'say': say}

        reply = 'cannot find place'
        print(self.data)
        return {'display': reply, 'say': reply}


# a = Report().display_place('nigeria')
# print(a)