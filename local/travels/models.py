from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TravelPost(models.Model):
  title = models.CharField(max_length=30)
  content = models.TextField()
  nation = models.TextField()
  city = models.TextField()
  together = models.IntegerField(default=1)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()
  create_date = models.DateTimeField(auto_now_add=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  views = models.IntegerField(default=0)
  likes = models.ManyToManyField(User, related_name='TravelLikes', blank=True)

  def __str__(self):
    return self.title
  
class TravelPhoto(models.Model):
  travel = models.ForeignKey(TravelPost, on_delete=models.CASCADE, null=True, blank=True)
  image = models.ImageField(upload_to='travels/', blank=True, null=True)
  
  
class TravelComment(models.Model):
  travel = models.ForeignKey(TravelPost, on_delete=models.CASCADE)
  author = models.ForeignKey(User, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField(auto_now_add=True)
