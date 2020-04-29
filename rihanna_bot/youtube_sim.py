from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from rihanna_bot import youtube_data

ps = PorterStemmer()

stop_words = set(stopwords.words("english"))


def remove_stopwords(enter_words):
    words = word_tokenize(enter_words)
    stemmed = [ps.stem(w) for w in words]
    filt_sen = ' '.join([w for w in stemmed if not w in stop_words])
    return train(filt_sen)


def train(sentence):
    documents = tuple([sentence]+list(youtube_data.yt_data.keys()))
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


def youtube_sim_main(word):
    y = similarity(word)
    if y == -1:
        return 0
    else:
        vid_ind = yt_d[y]              # video index
        return youtube_data.yt_data[vid_ind]                   # returns video dictionary


yt_d = list(youtube_data.yt_data.keys())

# a = youtube_sim_main('zodiac signs drake')
# print(a)