from django.urls import path

from apps.category import views

urlpatterns = [
    path('', views.CategoryListAPIView.as_view()),
    path('detail/<int:pk>/', views.CategoryDetailAPIView.as_view()),
    path('create/', views.CategoryCreateAPIView.as_view()),
    path('update/<int:pk>/', views.CategoryUpdateAPIView.as_view()),
    path('delete/<int:pk>/', views.CategoryDeleteAPIView.as_view()),
]
