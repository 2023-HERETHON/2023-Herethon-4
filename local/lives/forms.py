from django import forms
from .models import VideoComment

class VideoCommentForm(forms.ModelForm):
  content = forms.CharField(widget=forms.TextInput)
  content.label = '' 
  class Meta:
    model = VideoComment
    fields = ('content',)
    labels = {'content': ''}
