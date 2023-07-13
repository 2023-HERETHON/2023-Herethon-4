from django import forms
from .models import VideoComment

class VideoCommentForm(forms.ModelForm):
  class Meta:
    model = VideoComment
    fields = ('content',)
