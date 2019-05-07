"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from order import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r"^reg/$", views.register),
    url(r'^login/', views.login),
    url(r'^check_username_exist/', views.check_username_exist),
    url(r'^get_valid_img.png/', views.get_valid_img),
    url(r'^logout/',views.logout),
    url(r"^index/",views.index),
    url(r"^yuding/(\d+)/(\d+)/(\d+)",views.yuding),
    url(r"^kefu_yuding/(\d+)/(\d+)/(\w+)",views.kefu_yuding),
    url(r"^user_order/(\d+)",views.user_order),
    url(r"^re_password/(\w+)",views.re_password),
    url(r'^kefu_index/',views.kefu_index),
    url(r"^find_e/",views.get_kongfang),
    url(r"^kefu_order/(\d+)",views.kefu_order),
    url(r"kefu_tuiding/(\w+)/(\w+)",views.kefu_tuiding),
    url(r"^change_status/(\d+)/(\w+)",views.change_status),
]
