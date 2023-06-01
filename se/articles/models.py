from django.db import models
from django.contrib.auth.models import User
from mdeditor.fields import MDTextField

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name: models.CharField = models.CharField(max_length=100)
    first_name: models.CharField = models.CharField(max_length=100)
    klass: models.IntegerField = models.IntegerField()
    account_image: models.ImageField = models.ImageField(upload_to="profile_pics",blank=True)

    def __str__(self) -> str:
        return self.user.username

class Article(models.Model):
    title: models.CharField = models.CharField(max_length=100)    
    content: MDTextField = MDTextField()