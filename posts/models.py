from django.db import models
from account.models import UserData


class Post(models.Model):
    author = models.ForeignKey(UserData, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=800)


class Like(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    action = models.CharField(
        choices=[("like", "like"), ("unlike", "unlike")], max_length=10
    )
