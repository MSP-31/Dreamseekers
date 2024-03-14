from django.urls import include,path
from .views import inquiry,inquiry_index,inquiry_detail,lecture_calender,calenderUpdate,calenderDel

app_name = 'lecture'

urlpatterns = [
    # 상담 문의
    path('inquiry',inquiry, name='inquiry'),
    path('inquiry/list',inquiry_index,name='inquiry_index'),
    path('inquiry/list/<int:pk>/',inquiry_detail,name='inquiry_detail'),
    path('inquiry/comments/', include('comment.urls')),
    
    # 캘린더
    path('calender',lecture_calender,name='lecture_calender'),
    path('calender/update/<int:pk>/',calenderUpdate,name='calenderUpdate'),
    path('calender/del/<int:pk>/',calenderDel,name='calenderDel'),
]
