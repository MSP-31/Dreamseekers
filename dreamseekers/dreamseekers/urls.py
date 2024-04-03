from django.contrib import admin
from django.urls import path, include

from main.views import main

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),

    # 로그인
    path('user/',include('user.urls')),
    path('social/',include('user.API.urls')),

    # 교육원 소개
    path('intro/',include('intro.urls')),

    # 강의 문의
    path('lecture/',include('lecture.urls')),

    # 소통마당
    path('board/archive/',include('archive.urls')),
    path('board/notice/',include('notice.urls')),
    path('board/guest/',include('board.urls')),
    path('board/news/',include('blog.urls')),
]

# 이미지 url 설정
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
