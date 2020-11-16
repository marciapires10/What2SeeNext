from django.shortcuts import render
from lxml import etree
import sys
import os
from django.http import HttpResponse
import requests

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

    return render(request, 'movies_list.html')


def series(request):

    return render(request, 'series_list.html')