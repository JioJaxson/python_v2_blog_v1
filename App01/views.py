from django.shortcuts import render
from django.http import JsonResponse
import json


# 类似router
# Create your views here.
def index(request):
    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


def login(request):
    if request.method == 'POST':
        data = request.body  # 请求体
        dict_data = json.loads(data, encoding='utf8')
        print('data', data)
        print('dict_data', dict_data)
        print(dict_data.get('name'))
        return JsonResponse(request.POST)
    return render(request, 'login.html')


def sign(request):
    return render(request, 'sign.html')
