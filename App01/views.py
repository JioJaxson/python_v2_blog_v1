from django.shortcuts import render

# Create your views here.
def index(request):
    img_list = [
        "http://127.0.0.1:8000/media/site_bg/31.jpg",
        "http://127.0.0.1:8000/media/site_bg/29.jpg",
    ]

    return render(request,'index.html',{'img_list':img_list})
