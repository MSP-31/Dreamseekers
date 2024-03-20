from django.urls import path
from .views import greeting
from .views import instructors, instrs_delete, instrs_update
from .views import contact

app_name = 'intro'

urlpatterns = [
    # 인사말
    path('greeting/',greeting, name='greeting'),

    # 강사소개
    path('instructors/',instructors,name='instructors'),
    path('instructors/update/<int:pk>',instrs_update,name="instrs_update"),
    path('instructors/delete/<int:pk>',instrs_delete,name="instrs_del"),

    # 오시는 길
    path('contact/',contact, name="contact"),
]