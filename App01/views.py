from django.shortcuts import render

# Create your views here.
def index(request):
    img_list = [
        "../media/site_bg/31.jpg",
        "../media/site_bg/29.jpg",
        "../media/site_bg/28.jpg",
    ]

    return render(request,'index.html',{'img_list':img_list})
