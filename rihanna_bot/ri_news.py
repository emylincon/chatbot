from newsapi import NewsApiClient
import urllib.request
import urllib.parse
import config
import json

endpoints = ['/v2/top-headlines', '/v2/everything', '/v2/sources']

lang = ['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh']


def selector(query):
    if query[:len('news headline in ')] == 'news headline in ':      # news headline in uk
        country = query[len('news headline in '):]
        return News(country=country).headlines()
    elif query[:len('news headline search ')] == 'news headline search ':       # news headline search trump in uk
        msg = query[len('news headline search '):].split(' in ')
        return News(country=msg[1], search=msg[0]).headlines()
    elif query[:len('news headline with category ')] == 'news headline with category ':  # news headline with category business in uk
        msg = query[len('news headline with category '):].split(' in ')
        return News(country=msg[1], category=msg[0]).headlines()
    elif query[:] == 'news categories':
        return News().get_categories
    elif query == 'news headline':
        return News().headlines()
    else:
        reply = 'the requested query cannot be processed by rihanna news'
        return {'display': reply, 'say': reply}


class News:
    def __init__(self, search=None, country='united kingdom', category='general'):
        self.countries = {'argentina': 'ar', 'australia': 'au', 'austria': 'at', 'belgium': 'be', 'brazil': 'br',
                          'bulgaria': 'bg', 'canada': 'ca', 'china': 'cn', 'colombia': 'co', 'cuba': 'cu',
                          'czech republic': 'cz', 'egypt': 'eg', 'france': 'fr', 'germany': 'de', 'greece': 'gr',
                          'hong kong': 'hk', 'hungary': 'hu', 'india': 'in', 'indonesia': 'id', 'ireland': 'ie',
                          'israel': 'il', 'italy': 'it', 'japan': 'jp', 'latvia': 'lv', 'lithuania': 'it',
                          'malaysia': 'my', 'mexico': 'mx', 'morocco': 'ma', 'netherlands': 'nl', 'new zealand': 'nz',
                          'nigeria': 'ng', 'norway': 'no', 'philippines': 'ph', 'poland': 'pl', 'portugal': 'pt',
                          'romania': 'ro', 'russia': 'ru', 'saudi arabia': 'sa', 'serbia': 'rs', 'singapore': 'sg',
                          'slovakia': 'sk', 'slovenia': 'si', 'south africa': 'za', 'south korea': 'kr', 'sweden': 'se',
                          'switzerland': 'ch', 'taiwan': 'tw', 'thailand': 'th', 'turkey': 'tr', 'uae': 'ae',
                          'ukraine': 'ua', 'united kingdom': 'gb', 'united states': 'us', 'venuzuela': 've', 'uk': 'gb',
                          'us': 'us'}
        # request_headers = {
        #     "X-Api-Key": config.news_key,
        #     "Accept": "application/json",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"
        # }
        # pageURL = 'http://newsapi.org/v2/everything?q=coronavirus&from=2020-03-15&sortBy=publishedAt&language=en'
        # request = urllib.request.Request(pageURL, headers=request_headers)
        # contents = json.loads(urllib.request.urlopen(request).read())
        self.categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
        self.country = country
        self.search = search
        self.category = category
        self.newsapi = NewsApiClient(api_key=config.news_key)

    def headlines(self):
        if self.country in self.countries:
            top_headlines = self.newsapi.get_top_headlines(q=self.search,
                                                           category=self.category,
                                                           language='en',
                                                           country=self.countries[self.country])
            if self.category == 'general':
                display = f'<h1><font color="red">Top News in {self.country.upper()}</font></h1>'
            else:
                display = f'<h1><font color="red">Top {self.category.capitalize()} News in {self.country.upper()}</font></h1>'
            for article in top_headlines['articles'][:10]:
                image = article['urlToImage']
                source = article['source']['name']
                url = article['url']
                title = article['title']
                description = article['description']
                date = article['publishedAt'].split('T')
                # display += f'<a href="{url}" target="_blank"><h3>{title}</h3></a>'
                display += f"<table id='t01' style='table-layout:fixed; width:700px'>\
                      <tr>\
                        <th onclick='open_link(" + f'"{url}"' + f")'>" \
                        f"<img src='{image}' alt='{source} image' width='700px'>" \
                           f"<br><b><font color='blue'>{title}</font></b></th>\
                      </tr>\
                    "
                display += f"<tr>\
                                <td onclick='open_link(" + f'"{url}"' + f")'>" \
                        f"<div style = 'width:700px; word-wrap: break-word'> {description} {article['content']}</div>" \
                           f"<br><font color='grey' size='2'>Published at {source} on {date[1][:-1]}, {date[0]}</font>" \
                           f"</td>\
                            </tr>"

            say = f'find the displayed top news in {self.country}'
            return {'display': display, 'say': say}

        else:
            return {'display': f'cannot find {self.country} country', 'say': f'cannot find {self.country} country'}

    @property
    def get_categories(self):
        cats = ', '.join(self.categories)
        reply = f'the news categories include {cats}'
        return {'display': reply, 'say': reply}

    def recovered(self):
        pass



# from newsapi import NewsApiClient
#
# # Init
# newsapi = NewsApiClient(api_key='ffea7cc10ec84fc4b492e5382da16500')
#
# # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                           sources='bbc-news,the-verge',
#                                           category='business',
#                                           language='en',
#                                           country='us')
#
# # /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       from_param='2017-12-01',
#                                       to='2017-12-12',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=2)
#
# # /v2/sources
# sources = newsapi.get_sources()
