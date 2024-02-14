from datetime import timedelta
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from comment.forms import CommentForm
from comment.models import Comment, PostCommetns
from comment.serializers import CommentSerializer

from .models import Inquiry
from user.models import Users
from .forms import InquiryForm

# 강의 상담 문의 작성
def inquiry(request):
    # 로그인 여부 확인
    if not request.session.get('user'):
        return redirect('accounts:login')
    
    # GET요청시 회원정보 넘겨줌
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
            return redirect(inquiry_detail,pk=new_inquiry.pk)
        else:
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = InquiryForm(request.POST)
    else:
        form = InquiryForm()
    return render(request, 'inquiry_write', {'form':form})

# 내 문의 내역
def inquiry_index(request):
    # 현재 로그인한 유저의 id값을 가져옴
    if (request.user.is_authenticated and request.user.is_staff):
        inquiry_list = Inquiry.objects.order_by('-created_at')

    # 해당 유저의 모든 문의내역을 불러오고 페이지에 가져옴
    else:
        user_id = request.session.get('user')
        inquiry_list = Inquiry.objects.filter(author__id=user_id).order_by('-created_at')
    
    page = request.GET.get('page') # 페이지

    # 출력하는 Post수 제한
    paginator = Paginator(inquiry_list,10)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger: # 페이지가 지정되지 않았을때
        page = 1
        page_obj = paginator.page(page)
    except EmptyPage: # 페이지 범위를 초과할때
        page = paginator.num_pages
        page_obj = paginator.page(page)
    
    leftIndex = (int(page) -5)
    if leftIndex <1:
        leftIndex = 1
    rightIndex = (int(page) +5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages
    
    custom_range = range(leftIndex, rightIndex+1)

    return render(request,'inquiry_index.html',{'page_obj':page_obj, 'paginator':paginator, 'custom_range':custom_range})

# 문의 내역 자세히 보기
def inquiry_detail(request,pk):
    # pk로 해당 문의내역 검색
    inquiry = Inquiry.objects.get(pk=pk)
    user_id = request.session.get('user')
    
    # 모델 명
    board_name = "inquiry"

    # 해당유저인지 확인 & 관리자는 접근가능
    if (user_id == inquiry.author.id) or (request.user.is_authenticated and request.user.is_staff):
        pass
    else:
        return HttpResponse('<script>alert("접근 권한이 없습니다.");history.back();</script>')
    
    post_comments = PostCommetns.objects.filter(inquiry=inquiry)
    comments = Comment.objects.filter(postcommetns__in=post_comments, parent=None)
    comment_form = CommentForm()

    # 댓글 직렬화
    serializer = CommentSerializer(comments, many=True)
    serialized_comments = serializer.data

    return render(request, 'inquiry_detail.html',{'post':inquiry, 'comments':serialized_comments,
                            'comment_form':comment_form,'board_name':board_name})
