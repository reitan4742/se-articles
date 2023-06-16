from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm, ArticleForm
from typing import Any, Union
from .models import Article
from django.contrib.auth.models import User
from uuid import UUID
from django.contrib import messages
from django.utils import timezone

def Login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        Id = request.POST.get("userid")
        Pass = request.POST.get("password")
        user = authenticate(username=Id, password=Pass)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("articles:index"))
            else:
                messages.error(request, "アカウントが有効ではありません")
                return render(request, "articles/login.html")
        else:
            messages.error(request, "ログインIDまたはパスワードが間違っています")
            return render(request, "articles/login.html")
    else:
        return render(request, "articles/login.html")

@login_required
def Logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("articles:login"))

@login_required
def index(request: HttpRequest) -> HttpResponse:
    params = {
        "UserID": request.user,
        "article_list": Article.objects.all(),
    }
    return render(request, "articles/index.html", context=params)

class AccountRegistration(TemplateView):
    def __init__(self) -> None:
        self.params: dict = {
            "AccountCreate":False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request, "articles/signup.html", context=self.params)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        self.params["account_form"] = AccountForm(data=request.POST)
        self.params["add_account_form"] = AddAccountForm(data=request.POST)
        if self.params["account_form"].is_valid() and self.params["add_account_form"].is_valid():
            account = self.params["account_form"].save()
            account.set_password(account.password)
            account.save()

            add_account = self.params["add_account_form"].save(commit=False)
            add_account.user = account

            if 'account_image' in request.FILES:
                add_account.account_image = request.FILES['account_image']

            add_account.save()

            self.params["AccountCreate"] = True

        else:
            print(self.params["account_form"].errors)

        return render(request,"articles/signup.html",context=self.params)

class Draft(LoginRequiredMixin, TemplateView):
    def __init__(self) -> None:
        self.params: dict = {
            "article_form": ArticleForm(),
        }

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.params["article_form"] = ArticleForm()
        return render(request, "articles/draft.html", context=self.params)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        self.params["article_form"] = ArticleForm(data=request.POST)
        if self.params["article_form"].is_valid():
            editor = User.objects.get(username=self.request.user)
            publish_time = timezone.now()
            Article.objects.create(user=editor, pub_date=publish_time, title=request.POST.get("title"), content=request.POST.get("content"))
            return HttpResponseRedirect(reverse("articles:index"))
        else:
            print(self.params["article_form"].errors)
        return render(request,"articles/draft.html",context=self.params)


@login_required
def Postview(request: HttpRequest, article_id: UUID) -> HttpResponse:
    article = get_object_or_404(Article, pk=article_id)
    return render(request, "articles/posts.html", {"article": article})