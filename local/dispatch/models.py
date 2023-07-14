from django.utils import timezone
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()

# Create your models here.
class Dispatch(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    city = models.CharField(max_length=50)
    country  = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='dispatch_photos/', blank=True, null=True)

class Comment(models.Model):
    article = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 작성자
    content = models.TextField()  # 댓글 내용
    created_date = models.DateTimeField(auto_now_add=True)  # 작성일
    def __str__(self):
        return self.content
