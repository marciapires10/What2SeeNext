from django.shortcuts import render
from lxml import etree
import sys
import os
from django.http import HttpResponse
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
NO_IMAGE = os.path.join(BASE_DIR, "webapp/files/NoImage.jpg")


def get_top_rated_movies():
    # create query instance
    movies_xml = os.path.join(BASE_DIR, "webapp/files/movies.xml")
    query = session.query(QUERY_TOP_MOVIES).execute()
    movies_list = []
    tree = etree.XML(query)
    movies = tree.xpath(".//movie")

    for movie in movies:
        movie_temp = []
        movie_temp.append(movie.find("original_title").text)
        movie_temp.append(movie.find("vote_average").text)
        if movie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + movie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        movie_temp.append(poster_url)

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
        serie_temp.append(serie.find("original_name").text)
        serie_temp.append(serie.find("vote_average").text)
        if serie.find("poster_path").text is not None:
            poster_url = IMAGES_SITE + serie.find("poster_path").text
        else:
            poster_url = NO_IMAGE
        serie_temp.append(poster_url)
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
    t_params = {'news': news,
                'top_movies': top_movies,
                'top_series': top_series
                }

    return render(request, 'index.html', t_params)

def get_movie_genres():
    # create query instance
    result = session.query(QUERY_MOVIE_GENRES).execute()

    mgenres = result.replace('<genres>', "").replace('<genre>', "").replace('</genre>', "").replace('</genres>', "")

    return mgenres

def movies(request):
    pxml = 'movies.xml'
    pxslt = 'movies-list.xsl'
    fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)

    tree = ET.parse(fxml)
    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)

    mgenres = get_movie_genres()
    print(mgenres)

    tparams = {
        'html': html,
        'movie_genres': mgenres,
    }

    return render(request, 'movies_list.html', tparams)

def series(request):
    pxml = 'series.xml'
    pxslt = 'series-list.xsl'
    fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)

    tree = ET.parse(fxml)
    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)
    tparams = {
        'html_series': html,
    }

    return render(request, 'series_list.html', tparams)

def detail_info(request):

    m_review = movie_review()

    tparams = {
        'html_review': m_review
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
