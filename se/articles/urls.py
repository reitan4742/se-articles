from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("home/", views.home, name="home"),
    path("register/", views.AccountRegistration.as_view(), name="register"),
]
