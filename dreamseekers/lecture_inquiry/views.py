from django.shortcuts import redirect, render
from .models import Inquiry

from user.models import Users

from .forms import InquiryForm

# 강의 상담 문의 작성
def inquiry(request):
    # 로그인 여부 확인
    if not request.session.get('user'):
        return redirect('accounts:login')
    
    elif request.method == 'GET':
        form = InquiryForm()

        user_id = request.session.get('user')
        user = Users.objects.get(pk = user_id)
        
        phon_num = user.phone
        phon_num = '{}-{}-{}'.format(phon_num[:3],phon_num[3:7],phon_num[7:])

        return render(request, 'inquiry_write.html', {'form':form,'users':user,'phon_num':phon_num})

    elif request.method == 'POST':
        form = InquiryForm(request.POST)

        if form.is_valid():
            user_id = request.session.get('user')
            user = Users.objects.get(pk = user_id)

            new_inquiry = Inquiry.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                author    = user
            )
            return render(request, 'inquiry_write.html', {'form':form})
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = InquiryForm(request.POST)
    else:
        form = InquiryForm()
    return render(request, 'inquiry_write.html', {'form':form})
