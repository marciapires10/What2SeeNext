from django.shortcuts import render
from lxml import etree
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
import requests
import lxml.etree as ET
from BaseXClient import BaseXClient
from EDC_Project.settings import BASE_DIR
import os

MOVIES_NEWS = "https://www.cinemablend.com/rss/topic/news/movies"
IMAGES_SITE = "http://image.tmdb.org/t/p/w200"
session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
QUERY_TOP_MOVIES = "import module namespace funcs = \"com.funcs.catalog\"; funcs:top-movies()"
QUERY_TOP_SERIES = "import module namespace funcs = \"com.funcs.catalog\"; funcs:top-series()"
QUERY_MOVIE_GENRES = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-mgenres()"
QUERY_SERIE_GENRES = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-sgenres()"
QUERY_SBY_GENRE = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-genre-series({})"
QUERY_MBY_GENRE = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-genre-movies({})"

NO_IMAGE = "../static/assets/img/NoImage.jpg"


def get_top_rated_movies():
    # create query instance
    movies_xml = os.path.join(BASE_DIR, "webapp/files/movies.xml")
    query = session.query(QUERY_TOP_MOVIES).execute()
    movies_list = []
    tree = etree.XML(query)
    movies = tree.xpath(".//movie")

    for movie in movies:
        movie_temp = []
        if movie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + movie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        if movie.find("id").text is not None:
            movie_id = movie.find("id").text
        else:
            movie_id = "Undefined"

        movie_temp.append(movie.find("original_title").text)
        movie_temp.append(movie.find("vote_average").text)
        movie_temp.append(poster_url)
        movie_temp.append(movie_id)
        print(movie_id)
        movies_list.append(movie_temp)

    return movies_list


def get_top_rated_series():
    # create query instance
    query = session.query(QUERY_TOP_SERIES).execute()
    series_list = []
    tree = etree.XML(query)

    series = tree.xpath(".//serie")
    for serie in series:
        serie_temp = []

        if serie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + serie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        if serie.find("id").text is not None:
            serie_id = serie.find("id").text
        else:
            serie_id = "Undefined"

        serie_temp.append(serie.find("original_name").text)
        serie_temp.append(serie.find("vote_average").text)
        serie_temp.append(poster_url)
        serie_temp.append(serie_id)
        series_list.append(serie_temp)

    return series_list

def get_rss():
    response = requests.get(MOVIES_NEWS)
    tree = etree.XML(response.text)
    movies = []
    items = tree.xpath(".//item")
    for item in items:
        if item.find("title") is not None and item.find("description") is not None:

            description = item.find("description").text.replace("<p>","")
            description = description.replace("</p>","")
            description = description.replace("<em>","")
            description = description.replace("</em>", "")

            movie = []
            movie.append(item.find("title").text)
            movie.append(description)

            if item.find("enclosure") is not None:
                movie.append(str(item.find("enclosure").get('url')))
            if item.find("guid") is not None:
                movie.append(item.find("guid").text)
            movies.append(movie)

    return movies


def index(request):
    top_movies = get_top_rated_movies()
    top_series = get_top_rated_series()
    news = get_rss()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        print(id)
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)


    t_params = {'news': news,
                'top_movies': top_movies,
                'top_series': top_series
                }

    return render(request, 'index.html', t_params)

def get_movie_genres():
    # create query instance
    result = session.query(QUERY_MOVIE_GENRES).execute()
    tree = etree.XML(result)
    mgenres = [genre.text for genre in tree.xpath(".//genre")]

    return mgenres

def movies(request, filter = None, order = None):

    if 'filter' in request.POST and filter is None and request.POST.get('checkbox'):
        myDict = dict(request.POST.lists())
        _filter = myDict['checkbox']
        return movies(request, _filter)
    elif 'filter' in request.POST and request.POST.get('checkbox'):
        query = session.query(QUERY_MBY_GENRE.format(str(filter))).execute()
        tree = etree.XML(query)
    else:
        pxml = 'movies.xml'
        fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
        tree = ET.parse(fxml)

    if 'search' in request.POST:
        str = request.POST.get('search', '')
        print(str)
        return HttpResponseRedirect('/search_results/' + str)

    pxslt = 'movies-list.xsl'
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)

    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)

    mgenres = get_movie_genres()

    tparams = {
        'html': html,
        'movie_genres': mgenres,
    }

    return render(request, 'movies_list.html', tparams)

def get_series_genres():
    # create query instance
    result = session.query(QUERY_SERIE_GENRES).execute()
    tree = etree.XML(result)
    sgenres = [genre.text for genre in tree.xpath(".//genre")]

    return sgenres


def series(request , filter = None, order = None):

    if 'filter' in request.POST and filter is None and request.POST.get('checkbox'):
        myDict = dict(request.POST.lists())
        _filter = myDict['checkbox']
        return series(request, _filter)
    elif 'filter' in request.POST and request.POST.get('checkbox'):
        query = session.query(QUERY_SBY_GENRE.format(str(filter))).execute()
        tree = etree.XML(query)
    else:
        pxml = 'series.xml'
        fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
        tree = ET.parse(fxml)


    pxslt = 'series-list.xsl'
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)


    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)

    sgenres = get_series_genres()
    tparams = {
        'html_series': html,
        'serie_genres': sgenres,
    }

    return render(request, 'series_list.html', tparams)

def detail_info(request, id):
    # create query instance
    query = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-fullinfo('" + id + "')"
    result = session.query(query).execute()
    print(result)
    tree = etree.XML(result)

    info_list = []
    for item in tree:
        info_tmp = []

        if item.tag == 'original_title':
            if item.text is not None:
                original_title = item.text
            else:
                original_title = "Undefined"
        if item.tag == ''
        print(item.tag)



    # info to list: <original_title> (<title>), <genres>, <release_date>, <runtime>, <spoken_languages>, <production_companies>, <poster_path>,
    # <adult>, <overview>, <vote_average>

    for i in info_movies:
        info_tmp = []
        if i.find('poster_path').text is not None:
            poster_url = IMAGES_SITE + i.find('poster_path').text
        else:
            poster_url = NO_IMAGE

        if i.find('runtime').text is not None:
            runtime = i.find('runtime').text
        else:
            runtime = "Undefined"

        if i.find('release_date').text is not None:
            release_date = i.find('release_date').text
        else:
            release_date = "Undefined"

        if i.find('genres//item') is not None and i.find('genres//item/name') is not None:
            genres = ""
            for item in i.find('genres'):
                genres += "[" + item.find('name').text + "]"
        else:
            genres = "Undefined"

        if i.find('overview').text is not None:
            overview = i.find('overview').text
        else:
            overview = "Undefined"

        info_tmp.append(i.find('original_title').text)
        info_tmp.append(i.find('vote_average').text)
        info_tmp.append(poster_url)
        info_tmp.append(runtime)
        info_tmp.append(release_date)
        info_tmp.append(genres)
        info_tmp.append(overview)

        info_list.append(info_tmp)
        print(info_list)

    m_review = movie_review()

    tparams = {
        'html_review': m_review,
        'result': info_list,
    }

    return render(request, 'info.html', tparams)

def movie_review():
    pxml = 'reviews.xml'
    pxslt = 'movie-reviews.xsl'
    fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)

    tree = ET.parse(fxml)
    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)

    return html

def get_search_results(request, str):
    if 'search' in request.POST:
        str = request.POST.get('search', '')
        print(str)
        return HttpResponseRedirect('/search_results/' + str)
    # create query instance

    query_m = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-search-movies('" + str + "')"
    query_s = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-search-series('" + str + "')"
    query_c = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-search-persons('" + str + "')"
    result_m = session.query(query_m).execute()
    result_s = session.query(query_s).execute()
    result_c = session.query(query_c).execute()
    tree_m = etree.XML(result_m)
    tree_s = etree.XML(result_s)
    tree_c = etree.XML(result_c)
    movies = tree_m.xpath(".//movie")
    movies_list = get_movies_search(movies)
    series = tree_s.xpath(".//serie")
    series_list = get_series_search(series)
    cast_movies = tree_c.xpath(".//movie")
    cast_series = tree_c.xpath(".//serie")
    cast_movies_list = get_movies_search(cast_movies)
    cast_series_list = get_series_search(cast_series)


    tparams = {
        'str': str,
        'result_movies': movies_list,
        'result_series': series_list,
        'result_cast_movies': cast_movies_list,
        'result_cast_series': cast_series_list
    }

    return render(request, 'search_result.html', tparams)

def get_series_search(series):
    series_list = []

    for serie in series:

        serie_temp = []
        if serie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + serie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        if serie.find("first_air_date").text is not None:
            release_date = serie.find("first_air_date").text
        else:
            release_date = "Undefined"
        if serie.find("genres").find("item") is not None and serie.find("genres").find("item").find(
                "name") is not None:
            genres = ""
            for item in serie.find("genres"):
                genres += "[" + item.find("name").text + "] "
        else:
            genres = "Undefined"
        if serie.find("overview").text is not None:
            overview = serie.find("overview").text
        else:
            overview = "Undefined"

        serie_temp.append(serie.find("name").text)
        serie_temp.append(serie.find("vote_average").text)
        serie_temp.append(poster_url)
        serie_temp.append(release_date)
        serie_temp.append(genres)
        serie_temp.append(overview)

        series_list.append(serie_temp)

    return series_list

def get_movies_search(movies):
    movies_list = []

    for movie in movies:

        movie_temp = []
        if movie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + movie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        if movie.find("runtime").text is not None:
            runtime = movie.find("runtime").text
        else:
            runtime = "Undefined"
        if movie.find("release_date").text is not None:
            release_date = movie.find("release_date").text
        else:
            release_date = "Undefined"
        if movie.find("genres").find("item") is not None and movie.find("genres").find("item").find(
                "name") is not None:
            genres = ""
            for item in movie.find("genres"):
                genres += "[" + item.find("name").text + "] "
        else:
            genres = "Undefined"
        if movie.find("overview").text is not None:
            overview = movie.find("overview").text
        else:
            overview = "Undefined"

        movie_temp.append(movie.find("original_title").text)
        movie_temp.append(movie.find("vote_average").text)
        movie_temp.append(poster_url)
        movie_temp.append(runtime)
        movie_temp.append(release_date)
        movie_temp.append(genres)
        movie_temp.append(overview)

        movies_list.append(movie_temp)

        print(movies_list)

    return movies_list