from django.urls import include, path
from .views import index, post_detail, post_write, post_update, post_delete

#app_name = 'board'

urlpatterns = [
    path('',index, name='index'),
    path('<int:pk>/',post_detail,name='post_detail'),
    path('write/',post_write, name='post_write'),
    path('<int:pk>/update/',post_update, name='post_update'),
    path('<int:pk>/remove/',post_delete, name='post_delete'),

    path('comment/', include('comment.urls')),
]
