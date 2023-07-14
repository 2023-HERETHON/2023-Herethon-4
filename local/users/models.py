from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

class Profile(models.Model) :
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_provider = models.BooleanField(default=False)
    profile_photo = models.ImageField(blank=True, null=True, upload_to='profile_photo/')

    name = models.CharField(max_length=16, blank=False, default='')
    nickname = models.CharField(max_length=64, unique=True, blank=False, default='')
    phone = models.CharField(max_length=32, blank=False, default='')
    ticket_num = models.PositiveIntegerField(default=3)

    cntry_residence = models.CharField(max_length=32, blank=False, default='')
    city_residence = models.CharField(max_length=32, blank=False, default='')

    visited_cntry = models.CharField(max_length=64, blank=False, default='')
    visited_city = models.CharField(max_length=64, blank=False, default='')

    preferred_cntry = models.CharField(max_length=64, blank=False, default='')
    preferred_city = models.CharField(max_length=64, blank=False, default='')

    followers = models.ManyToManyField(User, related_name='followers')
    followings = models.ManyToManyField(User, related_name='followings')

    def __str__(self): 
        return self.nickname