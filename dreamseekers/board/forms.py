from django import forms
from board.models import Post

class BoardForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'contents','is_private']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'width'}),
            'contents': forms.Textarea(attrs={'class': 'width'}),
        }