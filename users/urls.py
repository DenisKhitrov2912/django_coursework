from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, LogoutView, RegisterView, email_verification, UserUpdateView, UserPasswordResetView, \
    UserPasswordSentView, UserListView, UserDetailView, UserMngUpdateView

app_name = UsersConfig.name




urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('email/verification/<str:token>/', email_verification, name='email_verification'),
    path('profile/', UserUpdateView.as_view(), name='profile'),
    path('password_reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('user_password_sent/', UserPasswordSentView.as_view(), name='user_password_sent'),
    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>', UserMngUpdateView.as_view(template_name='users/user_update.html'), name='user_update'),
]
