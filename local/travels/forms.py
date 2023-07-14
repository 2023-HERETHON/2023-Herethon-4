from django import forms
from .models import TravelComment

class TravelCommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.TextInput)
  content.label = '' 
  class Meta:
    model = TravelComment
    fields = ('content',)
    labels = {'content': ''}
