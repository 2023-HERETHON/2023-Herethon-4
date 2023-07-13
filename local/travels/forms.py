from django import forms
from .models import TravelComment

class TravelCommentForm(forms.ModelForm):
  class Meta:
    model = TravelComment
    fields = ('content',)
