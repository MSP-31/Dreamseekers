from django.urls import path
from .views import comments_create, comments_update, comments_delete, comments_nested

app_name = 'comment'

urlpatterns = [
    path('<str:board_name>/<int:pk>/',comments_create, name='comments_create'),
    path('<int:post_pk>/comment/<int:comment_pk>/update/',comments_update, name = 'comments_update'),
    path('comment/<int:comment_pk>/delete/',comments_delete, name = 'comments_delete'),
    path('<str:board_name>/<int:post_pk>/<int:comment_pk>/nested/',comments_nested, name = 'comments_nested'),
]
