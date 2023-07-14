from django import forms
from .models import dispatch, Comment

class dispatchForm(forms.ModelForm):
    class Meta:
        model = dispatch
        fields = ('city', 'country','content','photo')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content':'댓글내용',
        }
        # fields = '__all__'
        # exclude = ('article', 'user',)