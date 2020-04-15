from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

ps = PorterStemmer()

stop_words = set(stopwords.words("english"))


def remove_stopwords(enter_words):
    words = word_tokenize(enter_words)
    stemmed = [ps.stem(w) for w in words]
    filt_sen = ' '.join([w for w in stemmed if not w in stop_words])
    return train(filt_sen)


def train(sentence):
    documents = (
        sentence,
        'hot 100', 'billboard 200', 'artist 100', 'social 50', 'stream song', 'radio song', 'digit song sale', 'demand song', 'top album sale', 'current album', 'catalog album', 'independ album', 'soundtrack', 'vinyl album', 'greatest billboard 200 album', 'greatest billboard 200 artist', 'greatest hot 100 singl', 'greatest hot 100 artist', 'greatest hot 100 song women', 'greatest hot 100 women artist', 'greatest billboard 200 album women', 'greatest billboard 200 women artist', 'greatest billboard top song 80', 'greatest billboard top song 90', 'greatest time pop song', 'greatest time pop song artist', 'greatest adult pop song', 'greatest adult pop artist', 'greatest countri song', 'greatest countri album', 'greatest countri artist', 'greatest hot latin song', 'greatest hot latin song artist', 'greatest top danc club artist', 'greatest r b hip hop song', 'greatest r b hip hop album', 'greatest r b hip hop artist', 'greatest altern song', 'greatest altern artist', 'pop song', 'adult contemporari', 'adult pop song', 'countri song', 'countri album', 'countri stream song', 'countri airplay', 'countri digit song sale', 'bluegrass album', 'americana folk album', 'rock song', 'rock album', 'rock stream song', 'rock airplay', 'rock digit song sale', 'altern song', 'altern album', 'tripl', 'hot mainstream rock track', 'hard rock album', 'r b hip hop song', 'r b hip hop album', 'r b hip hop stream song', 'hot r b hip hop airplay', 'hot r b hip hop recurr airplay', 'r b hip hop digit song sale', 'r b song', 'r b album', 'r b stream song', 'r b digit song sale', 'rap song', 'rap album', 'rap stream song', 'hot rap track', 'rap digit song sale', 'mainstream r b hip hop', 'hot adult r b airplay', 'rhythmic 40', 'latin song', 'latin album', 'latin stream song', 'latin airplay', 'latin digit song sale', 'region mexican album', 'latin region mexican airplay', 'latin pop album', 'latin pop airplay', 'tropic album', 'latin tropic airplay', 'latin rhythm album', 'latin rhythm airplay', 'danc electron song', 'danc electron album', 'danc electron stream song', 'danc electron digit song sale', 'hot danc airplay', 'danc club play song', 'christian song', 'christian album', 'christian stream song', 'christian airplay', 'christian digit song sale', 'hot christian adult contemporari', 'gospel song', 'gospel album', 'gospel stream song', 'gospel airplay', 'gospel digit song sale', 'classic album', 'classic crossov album', 'tradit classic album', 'jazz album', 'contemporari jazz', 'tradit jazz album', 'jazz song', 'emerg artist', 'heatseek album', 'lyricfind global', 'lyricfind us', 'next big sound 25', 'hot holiday song', 'holiday album', 'holiday stream song', 'holiday song', 'holiday season digit song sale', 'summer song', 'canadian hot 100', 'canadian album', 'hot canada digit song sale', 'canada emerg artist', 'canada ac', 'canada format airplay', 'canada chr top 40', 'canada countri', 'canada hot ac', 'canada rock', 'mexico', 'mexico ingl', 'mexico popular', 'mexico espanol', 'japan hot 100', 'k pop hot 100', 'billboard china social chart', 'billboard argentina hot 100', 'offici uk song', 'offici uk album', 'uk digit song sale', 'euro digit song sale', 'franc digit song sale', 'germani song', 'german album', 'greec album', 'itali album', 'itali digit song sale', 'spain digit song sale', 'switzerland digit song sale', 'australian album', 'australia digit song sale', 'blue album', 'bubbl hot 100 singl', 'cast album', 'comedi album', 'compil album', 'hot singl recurr', 'kid album', 'new age album', 'regga album', 'tastemak album', 'world album', 'world digit song sale'

    )
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    array = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    return array[0][1:]


def similarity(phrase):
    arr = remove_stopwords(phrase)
    max_sim = max(arr)
    ind = list(arr).index(max_sim)

    if max_sim > 0.50:
        return ind
    else:
        return -1


def sim_main(word):
    y = similarity(word)
    if y == -1:
        return 0
    else:
        return chart[y]


chart = ['hot-100', 'billboard-200', 'artist-100', 'social-50', 'streaming-songs', 'radio-songs', 'digital-song-sales', 'on-demand-songs', 'top-album-sales', 'current-albums', 'catalog-albums', 'independent-albums', 'soundtracks', 'vinyl-albums', 'greatest-billboard-200-albums', 'greatest-billboard-200-artists', 'greatest-hot-100-singles', 'greatest-hot-100-artists', 'greatest-hot-100-songs-by-women', 'greatest-hot-100-women-artists', 'greatest-billboard-200-albums-by-women', 'greatest-billboard-200-women-artists', 'greatest-billboards-top-songs-80s', 'greatest-billboards-top-songs-90s', 'greatest-of-all-time-pop-songs', 'greatest-of-all-time-pop-songs-artists', 'greatest-adult-pop-songs', 'greatest-adult-pop-artists', 'greatest-country-songs', 'greatest-country-albums', 'greatest-country-artists', 'greatest-hot-latin-songs', 'greatest-hot-latin-songs-artists', 'greatest-top-dance-club-artists', 'greatest-r-b-hip-hop-songs', 'greatest-r-b-hip-hop-albums', 'greatest-r-b-hip-hop-artists', 'greatest-alternative-songs', 'greatest-alternative-artists', 'pop-songs', 'adult-contemporary', 'adult-pop-songs', 'country-songs', 'country-albums', 'country-streaming-songs', 'country-airplay', 'country-digital-song-sales', 'bluegrass-albums', 'americana-folk-albums', 'rock-songs', 'rock-albums', 'rock-streaming-songs', 'rock-airplay', 'rock-digital-song-sales', 'alternative-songs', 'alternative-albums', 'triple-a', 'hot-mainstream-rock-tracks', 'hard-rock-albums', 'r-b-hip-hop-songs', 'r-b-hip-hop-albums', 'r-and-b-hip-hop-streaming-songs', 'hot-r-and-b-hip-hop-airplay', 'hot-r-and-b-hip-hop-recurrent-airplay', 'r-and-b-hip-hop-digital-song-sales', 'r-and-b-songs', 'r-and-b-albums', 'r-and-b-streaming-songs', 'r-and-b-digital-song-sales', 'rap-song', 'rap-albums', 'rap-streaming-songs', 'hot-rap-tracks', 'rap-digital-song-sales', 'mainstream-r-and-b-hip-hop', 'hot-adult-r-and-b-airplay', 'rhythmic-40', 'latin-songs', 'latin-albums', 'latin-streaming-songs', 'latin-airplay', 'latin-digital-song-sales', 'regional-mexican-albums', 'latin-regional-mexican-airplay', 'latin-pop-albums', 'latin-pop-airplay', 'tropical-albums', 'latin-tropical-airplay', 'latin-rhythm-albums', 'latin-rhythm-airplay', 'dance-electronic-songs', 'dance-electronic-albums', 'dance-electronic-streaming-songs', 'dance-electronic-digital-song-sales', 'hot-dance-airplay', 'dance-club-play-songs', 'christian-songs', 'christian-albums', 'christian-streaming-songs', 'christian-airplay', 'christian-digital-song-sales', 'hot-christian-adult-contemporary', 'gospel-songs', 'gospel-albums', 'gospel-streaming-songs', 'gospel-airplay', 'gospel-digital-song-sales', 'classical-albums', 'classical-crossover-albums', 'traditional-classic-albums', 'jazz-albums', 'contemporary-jazz', 'traditional-jazz-albums', 'jazz-songs', 'emerging-artists', 'heatseekers-albums', 'lyricfind-global', 'lyricfind-us', 'next-big-sound-25', 'hot-holiday-songs', 'holiday-albums', 'holiday-streaming-songs', 'holiday-songs', 'holiday-season-digital-song-sales', 'summer-songs', 'canadian-hot-100', 'canadian-albums', 'hot-canada-digital-song-sales', 'canada-emerging-artists', 'canada-ac', 'canada-all-format-airplay', 'canada-chr-top-40', 'canada-country', 'canada-hot-ac', 'canada-rock', 'mexico', 'mexico-ingles', 'mexico-popular', 'mexico-espanol', 'japan-hot-100', 'k-pop-hot-100', 'billboard-china-social-chart', 'billboard-argentina-hot-100', 'official-uk-songs', 'official-uk-albums', 'uk-digital-song-sales', 'euro-digital-song-sales', 'france-digital-song-sales', 'germany-songs', 'german-albums', 'greece-albums', 'italy-albums', 'italy-digital-song-sales', 'spain-digital-song-sales', 'switzerland-digital-song-sales', 'australian-albums', 'australia-digital-song-sales', 'blues-albums', 'bubbling-under-hot-100-singles', 'cast-albums', 'comedy-albums', 'compilation-albums', 'hot-singles-recurrents', 'kids-albums', 'new-age-albums', 'reggae-albums', 'tastemaker-albums', 'world-albums', 'world-digital-song-sales']
