from django.urls import path
from .views import index, posting, post_write, post_delete

urlpatterns = [
    path('',index, name="index"),
    path('<int:pk>/',posting,name='post'),
    path('write/',post_write, name='post_write'),
    path('<int:pk>/remove/',post_delete, name='post_delete'),
]
