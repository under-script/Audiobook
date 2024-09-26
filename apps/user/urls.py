from django.urls import path

from . import views
from .views import register, change_password, user_settings, verify_code

app_name = 'user_app'

urlpatterns = [
    # path('register/', register, name='register'),
    # path('change-password/', change_password, name='change-password'),
    # path('settings/', user_settings, name='user-settings'),
    # path('verify-code/', verify_code, name='verify_code'),
    path('categories', views.UserCategoryListAPIView.as_view()),
    path('category/detail/<int:pk>/', views.UserCategoryDetailAPIView.as_view()),
    path('category/create/', views.UserCategoryCreateAPIView.as_view()),
    path('category/update/<int:pk>/', views.UserCategoryUpdateAPIView.as_view()),
    path('category/delete/<int:pk>/', views.UserCategoryDeleteAPIView.as_view()),
]