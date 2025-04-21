from django.urls import path

from . import views

urlpatterns = [
    path('', views.GetInfo.as_view()),
    path('query/', views.GetTickerInfo.as_view()),
    path('ticker/info/', views.CompanyInfo.as_view()),
    path('ticker/img/', views.ticker_picture),
    path('ticker/details/', views.GetTickerDetails.as_view()),
    path('wishlist', views.WishlistStock.as_view()),
]
