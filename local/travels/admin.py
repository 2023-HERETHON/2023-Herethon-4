from django.contrib import admin
from .models import *

# Register your models here.

# Photo 클래스를 inline으로 나타낸다.
class TravelPhotoInline(admin.TabularInline):
  model = TravelPhoto

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리하는 한다. 
class TravelPostAdmin(admin.ModelAdmin):
  inlines = [TravelPhotoInline, ]

# Register your models here.
admin.site.register(TravelPost, TravelPostAdmin)