from django.shortcuts import render
from django.http import JsonResponse


# 类似router
# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


def login(request):
    if request.method == 'POST':
        print(request.POST)
        return JsonResponse(request.POST)
    return render(request, 'login.html')


def sign(request):
    return render(request, 'sign.html')
