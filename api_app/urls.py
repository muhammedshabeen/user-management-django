from django.urls import path
from .views import *

urlpatterns = [
   path('register',RegisterView.as_view(),name="register"),
   path('login',LoginView.as_view(),name="login"),
   path('profile',ProfileView.as_view(),name="profile"),
   path('password-change',PasswordChangeView.as_view(),name="password_change"),
   path('logout', LogoutView.as_view(), name='logout'),
   path('user-list', UserLists.as_view(), name='user_list'),
] 
