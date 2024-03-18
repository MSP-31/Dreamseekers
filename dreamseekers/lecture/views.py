from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers

from comment.forms import CommentForm
from comment.models import Comment, PostCommetns
from comment.serializers import CommentSerializer

from .models import Inquiry, lectureCalender, lectureList, lectureTitle
from .forms import CalenderForm, InquiryForm, lectureListForm, lectureTitleForm

# 강의 상담 문의 작성
def inquiry(request):
    # 로그인 여부 확인
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    # GET요청시 회원정보 넘겨줌
    elif request.method == 'GET':
        form = InquiryForm()
        user = request.user
        phon_num = None

        return render(request, 'inquiry_write.html', {'form':form,'users':user,'phon_num':phon_num})

    elif request.method == 'POST':
        form = InquiryForm(request.POST)

        if form.is_valid():
            print("성공")
            user = request.user

            new_inquiry = Inquiry.objects.create(
                phone     = form.cleaned_data['phone'],
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                author    = user
            )
            return redirect('lecture:inquiry_detail', new_inquiry.pk)
        else:
            print("실패")
            # 폼이 유효하지 않을 경우, 사용자가 입력한 데이터를 폼에 다시 채워 넣습니다.
            form = InquiryForm(request.POST)
    return render(request, 'inquiry_write.html', {'form':form})

# 내 문의 내역
def inquiry_index(request):
    # 현재 로그인한 유저의 id값을 가져옴
    if request.user.is_staff:
        inquiry_list = Inquiry.objects.order_by('-created_at')

    # 해당 유저의 모든 문의내역을 불러오고 페이지에 가져옴
    else:
        user_id = request.user.id
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
    user_id = request.user.id
    
    # 모델 명
    board_name = "inquiry"

    # 해당유저인지 확인 & 관리자는 접근가능
    if (user_id == inquiry.author.id) or (request.user.is_staff):
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

# 캘린더
def lecture_calender(request):
    # DB에서 이벤트 데이터 가져오기
    schedules = lectureCalender.objects.all()
    schedules_json = serializers.serialize('json', schedules)

    form = CalenderForm()
    
    # 일정 작성
    if request.method == 'POST':
        form = CalenderForm(request.POST)

        if form.is_valid():
            allDay = request.POST.get('allDay')
            if allDay is None:
                print('논논노')
                startTimeStr = request.POST['startTime']
                endTimeStr = request.POST['endTime']
                allDay = False
                print(allDay)
            else:
                startTimeStr = '00:00'
                endTimeStr = '00:00'
                allDay = True
                print(allDay)
            
            startTime = datetime.strptime(startTimeStr, '%H:%M').time()
            endTime = datetime.strptime(endTimeStr, '%H:%M').time()

            new_calender = lectureCalender.objects.create(
                contents   = form.cleaned_data['contents'],
                date       = request.POST['startDate'],
                startTime  = startTime,
                endTime   = endTime,
                allDay     = allDay,
            )
            return redirect('lecture:lecture_calender')
    return render(request, 'lecture_calender.html', {'form':form, 'schedules': schedules_json})

# 일정 수정
def calenderUpdate(request,pk):
    # DB에서 이벤트 데이터 가져오기
    schedules = lectureCalender.objects.all()
    schedules_json = serializers.serialize('json', schedules)

    # 관리자 여부 확인
    if not request.user.is_staff:
        return redirect('accounts:login')

    # 해당하는 일정 가져옴
    schedules = lectureCalender.objects.get(pk=pk)

    if request.method == 'POST':
        form = CalenderForm(request.POST, instance=schedules)
        if form.is_valid():
            allDay = request.POST.get('allDay')
            
            # 시간 가져옴
            if allDay is None:
                print('논논노')
                startTimeStr = request.POST['startTime']
                endTimeStr = request.POST['endTime']
                allDay = False
                print(allDay)
            else:
                startTimeStr = '00:00'
                endTimeStr = '00:00'
                allDay = True
                print(allDay)

            # 시간 형식으로 바꿈
            startTime = datetime.strptime(startTimeStr, '%H:%M').time()
            endTime = datetime.strptime(endTimeStr, '%H:%M').time()

            schedules.date       = request.POST['startDate']
            schedules.startTime  = startTime
            schedules.endTime   = endTime
            schedules.allDay     = allDay

            schedules.save()
            return redirect('lecture:lecture_calender')
    else:
        form = CalenderForm(instance=schedules)
    return render(request, 'lecture_calender.html', {'form': form, 'schedules': schedules_json})

# 일정 삭제 
def calenderDel(request,pk):
    schedules = lectureCalender.objects.get(pk=pk)

    if request.method == 'POST':
        schedules.delete()
        return redirect('lecture:lecture_calender')
    return render(request)

# 주요강의
def lecture_list(request):
    # 모든 강의 제목을 불러오고, 각각의 강의 제목에 연결된 강의 리스트를 쿼리합니다.
    lectureTitles = lectureTitle.objects.all()
    form = lectureTitleForm()
    if request.method == 'POST':
        form = lectureTitleForm(request.POST, request.FILES)

        if form.is_valid():
            print("성공")

            new_lecture = lectureTitle.objects.create(
                title     = form.cleaned_data['title'],
                contents  = form.cleaned_data['contents'],
                image     = request.FILES.get('image'),
            )
            return redirect('lecture:lecture_list')
    return render(request, 'lecture_list.html',{'form': form,'titles':lectureTitles})

# 주요강의 수정
def lecture_update(request,pk):
    # 관리자 여부 확인
    if not request.user.is_staff:
        return redirect('accounts:login')

    lecture = lectureTitle.objects.get(pk=pk)

    if request.method == 'POST':
        form = lectureTitleForm(request.POST,instance=lecture)
        if form.is_valid():
            form.save()
            return redirect('lecture:lecture_list')
    return redirect('lecture:lecture_list')

# 주요강의 삭제
def lecture_del(request,pk):
    lecture = lectureTitle.objects.get(pk=pk)

    if request.method == 'POST':
        lecture.delete()
        return redirect('lecture:lecture_list')
    return render(request)

# 강의 상세보기
def lecture_detail(request,pk):
    titles = lectureTitle.objects.all().prefetch_related('lecturelist_set')
    title_list = titles.filter(pk=pk)

    form = lectureListForm()
    if request.method == 'POST':
        form = lectureListForm(request.POST)

        if form.is_valid():
            new_lectureList = lectureList.objects.create(
                lecture_list_id = pk,
                title           = form.cleaned_data['title'],
            )
            return redirect('lecture:lecture_detail', pk=pk)
        
    return render(request, 'lecture_detail.html',{'form': form,'titles':titles, 'list':title_list})


