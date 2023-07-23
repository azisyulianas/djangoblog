# BLOG URLS
from django.urls import path

from blog import views

urlpatterns = [
    # Blog Urls
    path(r'', views.HomeViews.as_view(), name = 'index'),
    path(r'create', views.CreateViews.as_view(), name = 'create'),
    path(r'edit/<str:slug>', views.CreateViews.as_view(), name = 'edit'),
    path(r'delete/<str:slug>', views.delete, name = 'delete'),
    path(r'post/<str:slug>', views.SingelPostViews.as_view(), name = 'detail'),
    path(r'category/<str:category>', views.HomeViews.as_view(), name = 'category'),
    # Category Urls
    path(r'category', views.CategoryIndex.as_view(), name='indexcategory'),
    path(r'category/<str:slug>/edit', views.CategoryEdit.as_view(), name='editcategory'),
]