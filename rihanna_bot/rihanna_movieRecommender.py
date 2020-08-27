from rotten_tomatoes_client import RottenTomatoesClient, MovieBrowsingQuery, Service, Genre, SortBy, \
    MovieBrowsingCategory
import imdb
from rihanna_bot.ri_youtube import Youtube
from multiprocessing.pool import ThreadPool


def selector(message):
    msgs = message.split(',')
    return Recommend(genres=msgs).get_request()


class Recommend:
    def __init__(self, genres, services=None, min_rating=40):
        self.genres = genres
        self.min_rating = min_rating
        self.services = [Service.netflix, Service.amazon_prime] if services is True else None
        self.genres_dict = {'action': Genre.action, 'comedy': Genre.comedy, 'romance': Genre.romance}
        self.ia = imdb.IMDb()

    def get_request(self):
        try:
            genres = [self.genres_dict[cat] for cat in self.genres]
        except KeyError:
            genres = None
        query = MovieBrowsingQuery(minimum_rating=self.min_rating, maximum_rating=100,
                                   services=self.services,
                                   certified_fresh=False, genres=genres,
                                   sort_by=SortBy.popularity,
                                   category=MovieBrowsingCategory.all_dvd_and_streaming)
        result = RottenTomatoesClient.browse_movies(query=query)['results'][:15]
        display = self.display_request(result)
        say = 'Please find displayed result'
        return {'display': display, 'say': say}

    def display_request(self, result):
        pool = ThreadPool(processes=2)
        response = '<div id="movie-display" style="width:600px;">'
        for movie in result:
            response += '<div class="movie-div">'
            response += f'<div class="movie-title"> {movie["title"]} </div>'

            result_list = [pool.apply_async(self.ia.search_movie, (movie['title'],)),
                           pool.apply_async(Youtube().search_youtube, (f"{movie['title']} trailer",))]

            response += result_list[1].get()['display']
            date = f"{movie['dvdReleaseDate']} , {result_list[0].get()[0].data['year']}"
            
            response += f'<div class="movie-foot"> <div class="movie-year">{date}</div> <div class="movie-rating"><span class="material-icons">star_outline</span>{movie["tomatoScore"]}</div> <div class="movie-mpaa">{movie["mpaaRating"]}</div> </div>'
            response += '</div>'
        response += '</div>  &nbsp;'
        return response


# https://pypi.org/project/rotten_tomatoes_client/
# Give me some relatively shitty action, comedy, or romance movies on Netflix or Amazon Prime, sorted by popularity
# query = MovieBrowsingQuery(minimum_rating=35, maximum_rating=70, services=[Service.netflix, Service.amazon_prime],
#                            certified_fresh=False, genres=[Genre.action, Genre.comedy, Genre.romance], sort_by=SortBy.popularity,
#                            category=MovieBrowsingCategory.all_dvd_and_streaming)

# query1 = MovieBrowsingQuery(minimum_rating=35, maximum_rating=70, services=None,
#                             certified_fresh=True, genres=None, sort_by=SortBy.release,
#                             category=MovieBrowsingCategory.all_dvd_and_streaming)
#
# res = RottenTomatoesClient.browse_movies(query=query1)
#
#
# results = res['results'][:10]

# print(selector('action, comedy'))