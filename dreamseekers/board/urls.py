from django.urls import path
from .views import index, posting, write

urlpatterns = [
    path('',index, name="index"),
    path('<int:pk>/',posting,name='post'),
    path('write/',write, name='write'),
]
