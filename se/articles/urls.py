from django.urls import path
from . import views

app_name = "articles"
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path("signup/", views.AccountRegistration.as_view(), name="signup"),
    path("draft/", views.Draft.as_view(), name="draft"),
    path("<str:article_id>/posts", views.Postview, name="posts"),
    path("mypage/", views.Mypage, name="mypage")
]
