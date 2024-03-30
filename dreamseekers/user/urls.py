from django.urls import path
from .views import login_view, logout_view, signup
from .views import account, account_modify,account_del

app_name = 'accounts'

urlpatterns = [
    path('login/',login_view, name='login'),
    path('logout/',logout_view, name='logout'),
    path('signup/',signup,name='signup'),

    path('account/',account,name='account'),
    path('account/modify/',account_modify,name='account_modify'),
    path('account/modify/del',account_del,name='account_del'),
]
