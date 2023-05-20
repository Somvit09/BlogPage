from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.utils import timezone


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(default=timezone.now)
    # Add related_name to resolve the clash
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self) -> str:
        return self.username

 
class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True)
    body = models.TextField(max_length=7000)
    image_url = models.URLField(max_length=1000)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    api_author_name = models.CharField(max_length=200, null=True)
    post_url = models.URLField(max_length=1500, null=True)

    def __str__(self) -> str:
        return self.title

class Comment(models.Model):
    text = models.TextField(max_length=350)
    user_commentted = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user_commentted