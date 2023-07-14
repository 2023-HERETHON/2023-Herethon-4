from django import forms
from .models import TravelComment

class TravelCommentForm(forms.ModelForm):
  content = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': '댓글을 입력해주세요'})
    )
  content.label = '' 
  class Meta:
    model = TravelComment
    fields = ('content',)
    labels = {'content': ''}
