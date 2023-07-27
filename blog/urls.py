# BLOG URLS
from django.urls import path

from blog.views import viewsCategory, viewsBlog

urlpatterns = [
    # Blog Urls
    path(r'', viewsBlog.HomeViews.as_view(), name = 'index'),
    path(r'create', viewsBlog.CreateViews.as_view(), name = 'create'),
    path(r'edit/<str:slug>', viewsBlog.CreateViews.as_view(), name = 'edit'),
    path(r'delete/<str:slug>', viewsBlog.deletepost, name = 'delete'),
    path(r'post/<str:slug>', viewsBlog.SingelPostViews.as_view(), name = 'detail'),
    path(r'category/<str:category>', viewsBlog.HomeViews.as_view(), name = 'category'),
    # Category Urls
    path(r'category', viewsCategory.CategoryIndex.as_view(), name='indexcategory'),
    path(r'category/<str:slug>/edit', viewsCategory.CategoryEdit.as_view(), name='editcategory'),
]