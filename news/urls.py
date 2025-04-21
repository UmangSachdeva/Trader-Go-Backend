from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = "users"

urlpatterns = [
    path('stock/', views.GetStockNews.as_view(), name='stock_news'),
]
