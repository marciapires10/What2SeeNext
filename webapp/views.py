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
#session = BaseXClient.Session('localhost', 1984, 'admin', 'admin')
GET_TOP_QUERY = os.path.join(BASE_DIR, 'queries/bestRated.xq')
def get_top_rated_movies():
    # create query instance
    input = "for $i in 1 to 10 return <xml>Text { $i }</xml>"
    query = session.query(input)

    # loop through all results
    for typecode, item in query.iter():
        print("typecode=%d" % typecode)
        print("item=%s" % item)

    # close query object
    query.close()

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

    t_params = {'movies': movies}

    return t_params


def index(request):
    #get_top_rated_movies()
    t_params = get_rss()
    return render(request, 'index.html', t_params)


def movies(request):
    pxml = 'movies.xml'
    pxslt = 'movies-list.xsl'
    fxml = os.path.join(BASE_DIR, 'webapp/files/' + pxml)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + pxslt)

    tree = ET.parse(fxml)
    xslt = ET.parse(fxslt)
    transform = ET.XSLT(xslt)
    html = transform(tree)

    genres = get_movie_genres()

    tparams = {
        'html': html,
        'movie_genres': genres,
    }

    return render(request, 'movies_list.html', tparams)

def get_movie_genres():
    fname = 'movies.xml'
    pname = os.path.join(BASE_DIR, 'webapp/files/' + fname)
    xml = ET.parse(pname)
    info = []
    query = '//movie/genres/item/name'
    genres = xml.xpath(query)

    for g in genres:
        info.append(g.text)

    return info

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



