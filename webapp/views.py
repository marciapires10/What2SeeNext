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
QUERY_MORDER_GENRE = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-all-movies-ordered-genre({},{})"
QUERY_MORDER = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-all-movies-ordered({})"
QUERY_SORDER_GENRE = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-all-series-ordered-genre({},{})"
QUERY_SORDER = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-all-series-ordered({})"
QUERY_REVIEW_MOVIE =  "import module namespace funcs = \"com.funcs.catalog\";funcs:get-review({})"
QUERY_REVIEW_SERIE =  "import module namespace funcs = \"com.funcs.catalog\";funcs:get-sreview({})"
QUERY_ADD_REVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:insert-review(\'{}\',\"{}\",\"{}\")"
QUERY_ADD_SREVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:insert-sreview(\'{}\',\"{}\",\"{}\")"
QUERY_UPDATE_REVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:update-review(\'{}\',\"{}\",\"{}\")"
QUERY_UPDATE_SREVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:update-sreview(\'{}\',\"{}\",\"{}\")"
QUERY_DELETE_REVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:delete-review(\'{}\',\"{}\")"
QUERY_DELETE_SREVIEW = "import module namespace funcs = \"com.funcs.catalog\";funcs:delete-sreview(\'{}\',\"{}\")"

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
            serie_id = serie.find("id").text + ".s"
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
            if item.find("pubDate") is not None:
                movie.append(item.find("pubDate").text)
            movies.append(movie)

    return movies


def index(request):
    top_movies = get_top_rated_movies()
    top_series = get_top_rated_series()
    news = get_rss()

    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
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
    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)
    if filter is None and request.POST.get('checkbox'):
        myDict = dict(request.POST.lists())
        _filter = myDict['checkbox']
        if 'order' in myDict:
            _order = myDict['order'][0]
        else:
            _order = None
        return movies(request, _filter, _order)

    elif request.POST.get('checkbox'):
        if request.POST.get('order'):
            if order == "Average":
                query = session.query(QUERY_MORDER_GENRE.format(str(filter), 1)).execute()
            elif order == "Popularity":
                query = session.query(QUERY_MORDER_GENRE.format(str(filter), 2)).execute()
            else:
                query = session.query(QUERY_MORDER_GENRE.format(str(filter), 3)).execute()
            tree = etree.XML(query)
        else:
            query = session.query(QUERY_MBY_GENRE.format(str(filter))).execute()
            tree = etree.XML(query)
    else:
        if request.POST.get('order'):
            myDict = dict(request.POST.lists())
            order = myDict['order'][0]
            if order == "Average":
                query = session.query(QUERY_MORDER.format(1)).execute()
            elif order == "Popularity":
                query = session.query(QUERY_MORDER.format(2)).execute()
            else:
                query = session.query(QUERY_MORDER.format(3)).execute()
            tree = etree.XML(query)
        else:
            pxml = 'movies.xml'
            fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
            tree = ET.parse(fxml)

    if 'search' in request.POST:
        search_str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + search_str)

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
    if 'search' in request.POST:
        search_str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + search_str)
    if 'info-m' in request.POST:
        id = request.POST.get('info-m')
        id_serie = str(id) + ".s"
        detail_info(request, id_serie)
        return HttpResponseRedirect('/info/' + id_serie)
    if filter is None and request.POST.get('checkbox'):
        myDict = dict(request.POST.lists())
        _filter = myDict['checkbox']
        if 'order' in myDict:
            _order = myDict['order'][0]
        else:
            _order = None
        return series(request, _filter, _order)

    elif request.POST.get('checkbox'):
        if request.POST.get('order'):
            send_filter = str(filter).replace("&", "&amp;")
            if order == "Average":
                query = session.query(QUERY_SORDER_GENRE.format(send_filter, 1)).execute()
            elif order == "Popularity":
                query = session.query(QUERY_SORDER_GENRE.format(send_filter, 2)).execute()
            else:
                query = session.query(QUERY_SORDER_GENRE.format(send_filter, 3)).execute()
            tree = etree.XML(query)
        else:
            send_filter = str(filter).replace("&","&amp;")
            query = session.query(QUERY_SBY_GENRE.format(send_filter)).execute()
            tree = etree.XML(query)
    else:
        if request.POST.get('order'):
            myDict = dict(request.POST.lists())
            order = myDict['order'][0]
            if order == "Average":
                query = session.query(QUERY_SORDER.format(1)).execute()
            elif order == "Popularity":
                query = session.query(QUERY_SORDER.format(2)).execute()
            else:
                query = session.query(QUERY_SORDER.format(3)).execute()
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

    if 'search' in request.POST:
        req = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + req)

    id_original = id
    id_list = id.split(".")
    is_movie = True
    if len(id_list) == 2:
        print("Movie")
        is_movie = False
        id = id_list[0]
        query = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-fullserieinfo('" + id + "')"
    else:
        print("Serie")
        query = "import module namespace funcs = \"com.funcs.catalog\"; funcs:get-fullinfo('" + id + "')"
    result = session.query(query).execute()
    print(result)
    tree = etree.XML(result)

    info_list = []
    genres = ""
    cast_str = ""
    crew_str = ""
    epi_season = ""
    status = "Released"
    cast_is_found = False
    crew_is_found = False

    for item in tree:
        info_tmp = []

        if item.tag == 'original_title' or item.tag == 'original_name':
            if item.text is not None:
                original_title = item.text
            else:
                original_title = "Undefined"

        if item.tag == "poster_path":
            if item.text is not None:
                poster_url = IMAGES_SITE + item.text
            else:
                poster_url = NO_IMAGE
        if item.tag == "vote_average":
            if item.text is not None:
                vote_average = item.text
            else:
                vote_average = "Undefined"
        if item.tag == "status":
            if item.text is not None:
                status = item.text
            else:
                status = "Undefined"
        if item.tag == "runtime":
            if item.text is not None:
                runtime = item.text
            else:
                runtime = "Undefined"
        if item.tag == "release_date" or item.tag == "first_air_date":
            if item.text is not None:
                release_date = item.text
            else:
                release_date = "Undefined"
        if item.tag == "genre":
            if item.find("name") is not None:
                if item.find("name").text is not None:
                    genres += "[" + item.find("name").text + "] "
            elif item.text is not None:
                genres += "[" + item.text + "] "
        if item.tag == "overview":
            if item.text is not None:
                overview = item.text
            else:
                overview = "Undefined"
        if item.tag == "number_of_episodes":
            if item.text is not None:
                epi_season += item.text + " Episodes, "
            else:
                epi_season += "Undefined number of Seasons"
        if item.tag == "number_of_seasons":
            if item.text is not None:
                epi_season += item.text + " Seasons"
            else:
                epi_season += "Undefined number of Seasons."
        if item.tag == "credit":
            count = 0
            if item.find("cast") is not None:
                for cast in item.find("cast"):
                    if cast.find("character").text is not None and cast.find("original_name").text is not None:
                        if cast_is_found:
                            cast_str += ", " + cast.find("original_name").text + " (as " + cast.find(
                                "character").text + ")"
                        else:
                            cast_str += ", " + cast.find("original_name").text + " (as " + cast.find(
                                "character").text + ")"
                            cast_is_found = True
                        count += 1
                    if count >= 5:
                        break
            else:
                cast_str = "Undefined."
            if item.find("crew") is not None:
                for crew in item.find("crew"):
                    if crew.tag == "original_name":
                        if crew.text is not None:
                            if crew_is_found:
                                crew_str += ", " + crew.text
                            else:
                                crew_str += crew.text
                                crew_is_found = True
                    if crew.tag == "job":
                        if crew.text is not None:
                            crew_str += " (" + crew.text + ")"
            else:
                crew_str = "Undefined"

    info_tmp.append(str(is_movie))
    info_tmp.append(original_title)
    info_tmp.append(poster_url)
    info_tmp.append(vote_average)
    if is_movie:
        info_tmp.append(runtime)
    else:
        info_tmp.append(epi_season)
    info_tmp.append(status)
    info_tmp.append(release_date)
    info_tmp.append(genres)
    info_tmp.append(overview)
    info_tmp.append(cast_str)
    info_tmp.append(crew_str)
    info_list.append(info_tmp)

    review = get_review(id, is_movie)
    tparams = {
        'html_review': review,
        'result': info_list,
    }

    if request.POST.get('delete'):
        if is_movie:
            query = QUERY_DELETE_REVIEW.format(id, request.POST.get('delete'))
        else:
            query = QUERY_DELETE_SREVIEW.format(id, request.POST.get('delete'))
        session.query(query).execute()
        return HttpResponseRedirect('/info/' + id_original)

    if request.POST.get('username') and request.POST.get('comment'):
        if is_movie:
            query = QUERY_ADD_REVIEW.format(id, request.POST.get('username'), request.POST.get('comment'))
        else:
            query = QUERY_ADD_SREVIEW.format(id, request.POST.get('username'), request.POST.get('comment'))

        session.query(query).execute()
        return HttpResponseRedirect('/info/' + id_original)

    return render(request, 'info.html', tparams)

def get_review(id, is_movie):

    if not is_movie:
        query = QUERY_REVIEW_SERIE.format(id)
    else:
        query = QUERY_REVIEW_MOVIE.format(id)

    result = session.query(query).execute()
    tree = etree.XML(result)
    pxslt = 'movie-reviews.xsl'
    tree = etree.XML(result)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)
    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)
    return html

def get_search_results(request, str):
    if 'search' in request.POST:
        str = request.POST.get('search', '')
        return HttpResponseRedirect('/search_results/' + str)
    if 'show_info' in request.POST:
        res = request.POST.get('show_info')
        res_div = res.split(",")
        if res_div[0] == "True":
            id = res_div[1]
        else:
            id = res_div[1] + ".s"
        print(id)
        detail_info(request, id)
        return HttpResponseRedirect('/info/' + id)
    # create query instance
    # titulo, rating, poster, duracao, data, generos, resumo

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
        if serie.find("id").text is not None:
            id = serie.find("id").text
        else:
            id = "Undefined"
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

        serie_temp.append(id)
        serie_temp.append(serie.find("name").text)
        serie_temp.append(serie.find("vote_average").text)
        serie_temp.append(poster_url)
        serie_temp.append(release_date)
        serie_temp.append(genres)
        serie_temp.append(overview)
        serie_temp.append(False)
        series_list.append(serie_temp)

    return series_list

def get_movies_search(movies):
    movies_list = []

    for movie in movies:

        movie_temp = []
        if movie.find("id").text is not None:
            id = movie.find("id").text
        else:
            id = "Undefined"
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

        movie_temp.append(id)
        movie_temp.append(movie.find("original_title").text)
        movie_temp.append(movie.find("vote_average").text)
        movie_temp.append(poster_url)
        movie_temp.append(runtime)
        movie_temp.append(release_date)
        movie_temp.append(genres)
        movie_temp.append(overview)
        movie_temp.append(True)
        movies_list.append(movie_temp)

    return movies_list

def full_news(request):

    full_news = get_rss()

    tparams = {
        'full_news': full_news,
    }

    return render(request, 'news.html', tparams)
