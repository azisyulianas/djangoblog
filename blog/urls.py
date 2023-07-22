# BLOG URLS
from django.urls import path

from blog import views

urlpatterns = [
    path(r'', views.HomeViews.as_view(), name = 'index'),
    path(r'create', views.CreateViews.as_view(), name = 'create'),
    path(r'edit/<str:slug>', views.CreateViews.as_view(), name = 'edit'),
    path(r'delete/<str:slug>', views.delete, name = 'delete'),
    path(r'post/<str:slug>', views.SingelPostViews.as_view(), name = 'detail'),
    path(r'category/<str:category>', views.HomeViews.as_view(), name = 'category'),
    path(r'author/<str:author>', views.HomeViews.as_view(), name = 'author'),
]