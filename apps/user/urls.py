from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import CustomUserViewSet

# app_name = 'user_app'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('genres', views.UserCategoryListAPIView.as_view()),
    path('category/detail/<int:pk>/', views.UserCategoryDetailAPIView.as_view()),
    path('category/create/', views.UserCategoryCreateAPIView.as_view()),
    path('category/update/<int:pk>/', views.UserCategoryUpdateAPIView.as_view()),
    path('category/delete/<int:pk>/', views.UserCategoryDeleteAPIView.as_view()),
]
urlpatterns += router.urls
