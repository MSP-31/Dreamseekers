from django import forms
from board.models import Post, Comment

class BoardForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'contents','photo','is_private']
        error_messages = {
            'title' : {
                'required' : '제목을 입력해주세요',
                'max_length' : '제목은 50 글자 이하로 입력해야 합니다.',
            },
            'contents' : {
                'required' : '내용을 입력해주세요.',
                'max_length' : '내용은 3000 글자 이하로 입력해야 합니다.',
            },
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        #fields = '__all__'
        exclude = ('article', 'user','parent',)