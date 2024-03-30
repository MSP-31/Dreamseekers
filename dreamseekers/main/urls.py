from django.urls import path
from .views import main, slide_modify, slide_update, slide_del

urlpatterns = [
    path('',main, name="main"),

    path('user/admin/slide',slide_modify,name="slide_modify"),
    path('user/admin/slide/update/<int:pk>',slide_update,name='slide_update'),
    path('user/admin/slide/del/<int:pk>/',slide_del,name='slide_del'),
]
