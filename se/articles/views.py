from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import AccountForm, AddAccountForm
from typing import Any

def Login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        Id = request.POST.get("userid")
        Pass = request.POST.get("password")
        user = authenticate(username=Id, password=Pass)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse("articles:home"))
            else:
                return HttpResponse("アカウントが有効ではありません")
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    else:
        return render(request, "articles/login.html")

@login_required
def Logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return HttpResponseRedirect(reverse("articles:login"))

@login_required
def home(request: HttpRequest) -> HttpResponse:
    params = {"UserID": request.user,}
    return render(request, "articles/home.html", context=params)

class AccountRegistration(TemplateView):
    def __init__(self) -> None:
        self.params = {
            "AccountCreate":False,
            "account_form": AccountForm(),
            "add_account_form": AddAccountForm(),
        }
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.params["account_form"] = AccountForm()
        self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request, "articles/signup.html", context=self.params)
    
    def post(self,request: HttpRequest) -> HttpResponse:
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
