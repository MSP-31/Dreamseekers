from django import forms
from .models import Archive

class ArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ['title', 'contents','image','files']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'width'}),
            'contents': forms.Textarea(attrs={'class': 'width'}),
            'image': forms.FileInput(attrs={'required': False}),
            'files': forms.FileInput(attrs={'required': False}),
        }
        
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