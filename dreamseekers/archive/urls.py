from django.urls import path
from .views import index, detail, write, update, delete
from .views import ArchiveView

app_name = 'archive'

urlpatterns = [
    path('',index, name='index'),
    path('<int:pk>/',detail,name='detail'),
    path('write/',write, name='write'),
    path('<int:pk>/update/',update, name='update'),
    path('<int:pk>/remove/',delete, name='delete'),

    path('search', ArchiveView.as_view(), name='search'),
]