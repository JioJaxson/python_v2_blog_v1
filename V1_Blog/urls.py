"""V1_Blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from App01 import views
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('news/', views.news),
    path('login/', views.login),
    path('login/random_code/', views.get_random_code),
    path('sign/', views.sign),
    path('logout/', views.logout),
    path('backstage/', views.backstage),  # 后台个人中心
    path('backstage/add_article/', views.add_article),  # 后台添加文章
    path('backstage/edit_avatar/', views.edit_avatar),  # 后台修改头像
    path('backstage/reset_password/', views.reset_password),  # 后台重置密码
    re_path(r'^backstage/edit_article/(?P<nid>\d+)/', views.edit_article),  # 编辑文章
    re_path(r'^article/(?P<nid>\d+)/', views.article),  # 文章详情页
    re_path(r'^api/', include('api.urls')),  # 路由分发 将所有以api开头的请求分发到api中的rls.py中
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件路由配置

]
