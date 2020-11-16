from django.shortcuts import render

# Create your views here.


def index(request):

    return render(request, 'index.html')


def movies(request):

    return render(request, 'movies_list.html')


def series(request):

    return render(request, 'series_list.html')