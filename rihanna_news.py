import requests
import config


def bbc():
    # BBC news api
    main_url = f" https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={config.news_key}"

    # fetching data in json format
    open_bbc_page = requests.get(main_url).json()

    # getting all articles in a string article
    article = open_bbc_page["articles"]
    reply = "Top 5 BBC News :"

    nos = 1
    for ar in article[:5]:
        news = ar["title"]
        url = ar["url"]

        reply += f'\n{nos}. {news} |<a href={url} target="_blank">Read</a>'
        nos += 1

    return reply
