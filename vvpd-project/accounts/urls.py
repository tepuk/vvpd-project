from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserTypeRedirectView, LoginUser, ChangePassword


urlpatterns = [
    path('', UserTypeRedirectView.as_view(), name='user_type'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update/password/', ChangePassword.as_view(), name='password-reset'),
]
