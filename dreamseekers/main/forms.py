from django import forms
from .models import Slides

# 강의 추가 폼
class SlidesForm(forms.ModelForm):
    class Meta:
        model = Slides
        fields = ['title','contents','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'width'}),
            'contents': forms.Textarea(attrs={'class': 'width'}),
        }