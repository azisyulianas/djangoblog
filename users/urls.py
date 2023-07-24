from django.urls import path

from . import viewsAuth, viewsUser

urlpatterns = [
    # UserModel
    path(r'', viewsAuth.ListUser.as_view(), name='list'),
    path(r'user/<str:user>', viewsAuth.IndexUsers.as_view(), name='index'),
    path(r'user/<str:user>/edit', viewsAuth.UserEditViews.as_view(), name='edit'),
    # AuthModel
    path(r'login', viewsUser.LoginViews.as_view(), name='login'),
    path(r'logout', viewsUser.Logout, name='logout'),
    path(r'create', viewsUser.RegisterViews.as_view(), name='create'),
]