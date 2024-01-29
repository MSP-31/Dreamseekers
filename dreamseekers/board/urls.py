from django.urls import path
from .views import index, post_detail, post_write, post_update, post_delete
from .views import comments_create, comments_update, comments_delete, comments_nested

#app_name = 'boards'

urlpatterns = [
    path('',index, name="index"),
    path('<int:pk>/',post_detail,name='post_detail'),
    path('write/',post_write, name='post_write'),
    path('<int:pk>/update/',post_update, name='post_update'),
    path('<int:pk>/remove/',post_delete, name='post_delete'),

    path('<int:pk>/comments/',comments_create, name='comments_create'),
    path('<int:post_pk>/comments/<int:comment_pk>/update/',comments_update, name = 'comments_update'),
    path('<int:post_pk>/comments/<int:comment_pk>/delete/',comments_delete, name = 'comments_delete'),
    path('<int:post_pk>/comments/<int:comment_pk>/nested/',comments_nested, name = 'comments_nested'),
]
