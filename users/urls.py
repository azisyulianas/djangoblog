from django.urls import path

from .views import viewsAuth, viewsUsers

urlpatterns = [
    # UserModel
    path(r'', viewsUsers.ListUser.as_view(), name='list'),
    path(r'user/<str:user>', viewsUsers.IndexUsers.as_view(), name='index'),
    path(r'user/<str:user>/edit', viewsUsers.UserEditViews.as_view(), name='edit'),
    # AuthModel
    path(r'login', viewsAuth.LoginViews.as_view(), name='login'),
    path(r'logout', viewsAuth.Logout, name='logout'),
    path(r'create', viewsAuth.RegisterViews.as_view(), name='create'),
]