from django.contrib import admin
from django.urls import path
from api.views import login, article

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登陆
    path('sign/', login.SignView.as_view()),  # 注册
    path('article/', article.ArticleView.as_view()),  # 发布文章

]
