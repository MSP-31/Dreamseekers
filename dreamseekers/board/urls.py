from django.urls import path
from .views import index, posting

urlpatterns = [
    path('',index, name="index"),
    path('<int:pk>/',posting,name='post'),
]
