import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.co.uk/s?k="
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}





def search_amazon(query):
    req = url + query
    page = requests.get(req, headers=header)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all("div", {"class": "s-include-content-margin s-border-bottom"})
    item_dict = {}
    item_link = {}
    for i in items:
        _name = i.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).get_text()
        _price = float(i.find("span", {"class": "a-offscreen"}).get_text()[1:])
        _link = i.find("a", {"class": "a-link-normal a-text-normal"}).get('href')
        item_dict[_name] = _price
        item_link[_name] = _link
    return item_dict, item_link


def product_min_price(query):
    item_dict, item_link = search_amazon(query)
    min_price = min(item_dict, key=item_dict.get)
    reply = "<table>\
                  <tr>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Link</th>\
                  </tr>\
                "
    reply += f"<tr>\
                        <td>{min_price}</td>\
                        <td>£{item_dict[min_price]}</td>\
                        <td><a href='https://www.amazon.co.uk{item_link[min_price]}' target='_blank'>Follow Link</a></td>\
                      </tr>"
    return reply


def product_max_price(query):
    item_dict, item_link = search_amazon(query)
    max_price = max(item_dict, key=item_dict.get)
    reply = "<table>\
                  <tr>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Link</th>\
                  </tr>\
                "
    reply += f"<tr>\
                        <td>{max_price}</td>\
                        <td>£{item_dict[max_price]}</td>\
                        <td><a href='https://www.amazon.co.uk{item_link[max_price]}' target='_blank'>Follow Link</a></td>\
                      </tr>"
    return reply

