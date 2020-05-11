import datetime
from bs4 import BeautifulSoup
from selenium import webdriver


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
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
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
        if place in self.data:
            display = "<table id='t01'><tr>"
            display += f"<td><b>Place</b></td>"
            display += f"<td>{place.title()}</td></tr>"
            for value in self.data[place]:
                display += f"""<tr>
                              <td style='font-size:16px;'><b>{value}</b></td>
                              <td>{self.data[place][value]}</td>
                              </tr>"""
            display += '</table>'
            say = f"find covid19 details for {place} updated on {str(datetime.datetime.now()).split()[0]}"
            return {'display': display, 'say': say}
        else:
            reply = 'cannot find place'
            return {'display': reply, 'say': reply}


# a = Report().display_place('usa')
# print(a)