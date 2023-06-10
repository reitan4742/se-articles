from django import forms
from django.contrib.auth.models import User
from .models import Account, Article
from mdeditor.fields import MDTextFormField

class AccountForm(forms.ModelForm):
    password: forms.CharField = forms.CharField(widget=forms.PasswordInput(), label="パスワード")

    class Meta():
        model = User
        fields = ("username","email","password")
        labels = {"username":"ユーザID","email":"メール"}

class AddAccountForm(forms.ModelForm):
    class Meta():
        model = Account
        fields = ("last_name","first_name","klass","account_image",)
        labels = {"last_name":"苗字","first_name":"名前","klass":"期生","account_image":"写真アップロード",}

# class ArticleForm(forms.Form):
#     title: forms.CharField = forms.CharField()
#     content = MDTextFormField()

class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
    class Meta():
        model = Article
        fields = ("title","content",)
        labels = {"title":"タイトル","content":"記事",}