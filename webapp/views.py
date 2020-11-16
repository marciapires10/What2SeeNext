from django.shortcuts import render
from lxml import etree
import sys
import os
from django.http import HttpResponse
import requests
import lxml.etree as ET

from EDC_Project.settings import BASE_DIR

MOVIES_NEWS = "https://www.cinemablend.com/rss/topic/news/movies"


def get_rss(request):
    response = requests.get(MOVIES_NEWS)
    tree = etree.XML(response.text)
    titles = ""
    for item in tree.find("channel"):
        if item.find("title") is not None and item.find("description") is not None:
            titles += "\n-> Title: " + item.find("title").text + "\n" + item.find("description").text + "\n "

    return HttpResponse(titles)


def index(request):

    return render(request, 'index.html')


def movies(request):
    xml = 'movies.xml'
    xslt = 'movies-list.xsl'
    fxml = os.path.join(BASE_DIR, 'webapp/files/' + xml)
    fxslt = os.path.join(BASE_DIR, 'webapp/files/' + xslt)

    tree = ET.parse(fxml)
    xslt_parse = ET.parse(fxslt)
    transform = ET.XSLT(xslt_parse)

    tparams = {
        'html': transform,
    }

    return render(request, 'movies_list.html', tparams)


def series(request):

    return render(request, 'series_list.html')



