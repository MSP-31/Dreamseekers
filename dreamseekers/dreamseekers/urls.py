from django.contrib import admin
from django.urls import path, include

from main.views import main

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('/', include('main.urls')),
    path('user/',include('user.urls')),
    path('board/',include('board.urls')),
    path('lecture/',include('lecture_inquiry.urls')),
]

# 이미지 url 설정
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
