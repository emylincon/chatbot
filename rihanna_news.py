import requests
import config

def NewsFromBBC():
    # BBC news api
    main_url = f" https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey={config.news_key}"

    # fetching data in json format
    open_bbc_page = requests.get(main_url).json()

    # getting all articles in a string article
    article = open_bbc_page["articles"]
    print(article)

    # empty list which will
    # contain all trending news
    results = []

    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        # printing all trending news
        print(i + 1, results[i])

    # Driver Code


if __name__ == '__main__':
    # function call
    NewsFromBBC()