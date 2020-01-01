import requests
from bs4 import BeautifulSoup
import config

url = "https://www.amazon.co.uk/s?k="


def get_number(word):
    newstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in word)
    listOfNumbers = [float(i) for i in newstr.split()]
    return listOfNumbers[0]


def selector(msg):
    if msg[:len("amazon least price for")] == "amazon least price for":
        msg = msg[len("amazon least price for")+1:].strip()
        return product_min_price(msg)
    elif msg[:len("amazon max price for")] == "amazon max price for":
        msg = msg[len("amazon max price for")+1:].strip()
        return product_max_price(msg)
    elif msg[:len("amazon sort price for")] == "amazon sort price for":   # e.g amazon sort price for speakers at 11
        sub_msg = msg[len("amazon sort price for")+1:].strip()
        msg,price_raw = sub_msg.split(' at ')
        price = get_number(price_raw)
        return sort_products(msg, [price,0])
    elif msg[:len("amazon sort rating for")] == "amazon sort rating for":   # e.g amazon sort rating for speakers at 4.5
        sub_msg = msg[len("amazon sort rating for")+1:].strip()
        msg,rate_raw = sub_msg.split(' at ')
        rate = get_number(rate_raw)
        return sort_products(msg, [0,rate])
    else:
        return "We apologise on behalf of our brothers and sister in amazon.co.uk"


def search_amazon(query):
    req = url + query
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all("div", {"class": "s-include-content-margin s-border-bottom"})
    item_dict = {}
    item_link = {}     # item_link = {item: [item_link, image_link, rating]}
    for i in items:
        _name = i.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).get_text()
        _price = float(i.find("span", {"class": "a-offscreen"}).get_text()[1:])
        _link = i.find("a", {"class": "a-link-normal a-text-normal"}).get('href')
        _img = i.find("img", {"class": "s-image"}).get('src')
        _rate = i.find("span", {"class": "a-icon-alt"}).get_text()
        item_dict[_name] = _price
        item_link[_name] = [_link, _img, _rate]
    return item_dict, item_link


def product_min_price(query):
    item_dict, item_link = search_amazon(query)
    min_price = min(item_dict, key=item_dict.get)
    reply = "<table id='t01'>\
                  <tr>\
                    <th>Image</th>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Rating</th>\
                  </tr>\
                "
    reply += f"<tr>\
                        <td><img src='{item_link[min_price][1]}' alt='{query} image' width='40%' height='40%'></td>\
                        <td><a href='https://www.amazon.co.uk{item_link[min_price][0]}' target='_blank'>{min_price}</a></td>\
                        <td>£{item_dict[min_price]}</td>\
                        <td>{item_link[min_price][2]}</td>\
                      </tr>"
    return reply


def product_max_price(query):
    item_dict, item_link = search_amazon(query)
    max_price = max(item_dict, key=item_dict.get)
    reply = "<table id='t01'>\
                      <tr>\
                        <th>Image</th>\
                        <th>Product Name</th>\
                        <th>Price</th>\
                        <th>Rating</th>\
                      </tr>\
                    "
    reply += f"<tr>\
                            <td><img src='{item_link[max_price][1]}' alt='{query} image' width='40%' height='40%'></td>\
                            <td><a href='https://www.amazon.co.uk{item_link[max_price][0]}' target='_blank'>{max_price}</a></td>\
                            <td>£{item_dict[max_price]}</td>\
                            <td>{item_link[max_price][2]}</td>\
                          </tr>"
    return reply


def search_amazon_sort(query):
    req = url + query
    page = requests.get(req, headers=config.header)
    soup = BeautifulSoup(page.content, 'html.parser')
    items = soup.find_all("div", {"class": "s-include-content-margin s-border-bottom"})
    item_dict = {}
    item_link = {}  # item_link = {item: [item_link, image_link, rating]}
    item_rate = {}
    for i in items:
        _name = i.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).get_text()
        _price = float(i.find("span", {"class": "a-offscreen"}).get_text()[1:])
        _link = i.find("a", {"class": "a-link-normal a-text-normal"}).get('href')
        _img = i.find("img", {"class": "s-image"}).get('src')
        _rate = float(i.find("span", {"class": "a-icon-alt"}).get_text().split()[0])
        item_dict[_name] = _price
        item_link[_name] = [_link, _img]
        item_rate[_name] = _rate

    return item_dict, item_link, item_rate


def sort_products(query, _sort=(), no=5):  # _sort = [1,1]    [price, rate]
    reply = ''
    if len(_sort) == 0:
        item_dict, item_link, item_rate = search_amazon_sort(query)

        reply = "<table id='t01'>\
                  <tr>\
                    <th>Image</th>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Rating</th>\
                  </tr>\
                "
        for i in list(item_dict.keys())[:no]:
            reply += f"<tr>\
                          <td><img src='{item_link[i][1]}' alt='{query} image' width='40%' height='40%'></td>\
                          <td><a href='https://www.amazon.co.uk{item_link[i][0]}' target='_blank'>{i}</a></td>\
                          <td>£{item_dict[i]}</td>\
                          <td>{item_rate[i]}</td>\
                        </tr>"
    elif _sort[0] != 0:
        item_dict, item_link, item_rate = search_amazon_sort(query)
        sorted_price = {k: v for k, v in sorted(item_dict.items(), key=lambda item: item[1])}
        start = 0
        for i in sorted_price.values():
            if i >= _sort[0]:
                start = list(sorted_price.values()).index(i)
                break
            else:
                start = len(sorted_price)/2

        reply = "<table id='t01'>\
                  <tr>\
                    <th>Image</th>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Rating</th>\
                  </tr>\
                "
        if len(sorted_price) > (start + no):
            for i in list(sorted_price.keys())[start:start + no]:
                reply += f"<tr>\
                            <td><img src='{item_link[i][1]}' alt='{query} image' width='40%' height='40%'></td>\
                            <td><a href='https://www.amazon.co.uk{item_link[i][0]}' target='_blank'>{i}</a></td>\
                            <td>£{item_dict[i]}</td>\
                            <td>{item_rate[i]} / 5</td>\
                          </tr>"
        else:
            for i in list(sorted_price.keys())[start:]:
                reply += f"<tr>\
                            <td><img src='{item_link[i][1]}' alt='{query} image' width='40%' height='40%'></td>\
                            <td><a href='https://www.amazon.co.uk{item_link[i][0]}' target='_blank'>{i}</a></td>\
                            <td>£{item_dict[i]}</td>\
                            <td>{item_rate[i]} / 5</td>\
                          </tr>"

    elif _sort[1] != 0:
        item_dict, item_link, item_rate = search_amazon_sort(query)
        sorted_rate = {k: v for k, v in sorted(item_rate.items(), key=lambda item: item[1])}
        start = 0
        for i in sorted_rate.values():
            if i >= _sort[1]:
                start = list(sorted_rate.values()).index(i)
                break
            else:
                start = len(sorted_rate)/2

        reply = "<table id='t01'>\
                  <tr>\
                    <th>Image</th>\
                    <th>Product Name</th>\
                    <th>Price</th>\
                    <th>Rating</th>\
                  </tr>\
                "
        if len(sorted_rate) > (start + no):
            for i in list(sorted_rate.keys())[start:start + no]:
                reply += f"<tr>\
                            <td><img src='{item_link[i][1]}' alt='{query} image' width='40%' height='40%'></td>\
                            <td><a href='https://www.amazon.co.uk{item_link[i][0]}' target='_blank'>{i}</a></td>\
                            <td>£{item_dict[i]}</td>\
                            <td>{item_rate[i]} / 5</td>\
                          </tr>"
        else:
            for i in list(sorted_rate.keys())[start:]:
                reply += f"<tr>\
                            <td><img src='{item_link[i][1]}' alt='{query} image' width='40%' height='40%'></td>\
                            <td><a href='https://www.amazon.co.uk{item_link[i][0]}' target='_blank'>{i}</a></td>\
                            <td>£{item_dict[i]}</td>\
                            <td>{item_rate[i]} / 5</td>\
                          </tr>"
    return reply
