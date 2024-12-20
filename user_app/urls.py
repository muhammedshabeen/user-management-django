from django.urls import path
from .views import *

urlpatterns = [
    path('',signin,name='signin'),
    path('signup',signup,name='signup'),
    path('dashboard',dashboard,name='dashboard'),
    path('profile',profile,name='profile'),
    path('signout',signout,name='signout'),
    
    #ViewCustomer
    path('users-view',user_lists,name="user_lists"),
]
