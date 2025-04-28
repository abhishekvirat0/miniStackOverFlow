from django.urls import path

from users.views import RegisterUserView, loginview, userprofileview

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', loginview, name='login'),
    path('me/', userprofileview, name='user-profile'),
]
