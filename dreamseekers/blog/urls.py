from django.urls import path
from .views import search_blog

urlpatterns = [
    path('',search_blog, name='search_blog'),
]
