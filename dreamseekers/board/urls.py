from django.urls import path
from .views import index, posting, board_write

urlpatterns = [
    path('',index, name="index"),
    path('<int:pk>/',posting,name='post'),
    path('write/',board_write, name='board_write'),
]
