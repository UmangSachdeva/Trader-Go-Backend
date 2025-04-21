from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "users"

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('verify-email/', views.VerifyUserEmail.as_view(), name='verify'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('test/', views.TestRoute.as_view(), name='granted'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('verify', TokenVerifyView.as_view(), name="verify_token"),
    path('', views.GetUserDetails.as_view(), name="user_info")
]
