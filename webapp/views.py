from django.shortcuts import render
from lxml import etree
import sys
import os
from django.http import HttpResponse
import requests
import lxml.etree as ET

from EDC_Project.settings import BASE_DIR

MOVIES_NEWS = "https://www.cinemablend.com/rss/topic/news/movies"


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
    tparams = {
        'html': html,
    }

    return render(request, 'movies_list.html', tparams)


def series(request):

    return render(request, 'series_list.html')



