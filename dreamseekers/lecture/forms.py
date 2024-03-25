import re
from django import forms
from lecture.models import Inquiry, lectureCalender, lectureTitle, lectureList
from django.core.exceptions import ValidationError

# 강의 문의 폼
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['phone', 'title', 'contents']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'width'}),
            'contents': forms.Textarea(attrs={'class': 'width'}),
        }
        error_messages = {
            'phone' : {
                'required' : '연락처를 입력해주세요',
            },
            'title' : {
                'required' : '제목을 입력해주세요',
                'max_length' : '제목은 50 글자 이하로 입력해야 합니다.',
            },
            'contents' : {
                'required' : '내용을 입력해주세요.',
                'max_length' : '내용은 3000 글자 이하로 입력해야 합니다.',
            },
        }
        
    # 전화번호 검증
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # 전화번호 형식을 검증하는 정규 표현식
        phone_regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$'
        
        if not re.match(phone_regex, phone):
            raise ValidationError('올바른 전화번호 형식이 아닙니다.')
        return phone

# 강의 일정 폼
class CalenderForm(forms.ModelForm):
    class Meta:
        model = lectureCalender
        fields = ['contents']

# 강의 추가 폼
class lectureTitleForm(forms.ModelForm):
    class Meta:
        model = lectureTitle
        fields = ['title','contents','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'width'}),
            'contents': forms.Textarea(attrs={'class': 'width'}),
        }

# 강의 추가 폼
class lectureListForm(forms.ModelForm):
    class Meta:
        model  = lectureList
        fields = ['title']