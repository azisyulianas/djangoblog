from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.ListUser.as_view(), name='list'),
    path(r'login', views.LoginViews.as_view(), name='login'),
    path(r'logout', views.Logout, name='logout'),
    path(r'create', views.RegisterViews.as_view(), name='create'),
    path(r'user/<str:user>', views.IndexUsers.as_view(), name='index'),
    path(r'user/<str:user>/edit', views.UserEditViews.as_view(), name='edit'),
]