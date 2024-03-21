from django import forms
from comment.models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': '댓글을 입력하세요'}))

    class Meta:
        model = Comment
        #fields = '__all__'
        exclude = ('user','parent',)