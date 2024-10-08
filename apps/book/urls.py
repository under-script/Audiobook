from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from .views import FileUploadView

router = DefaultRouter()
router.register(r'', views.BookViewSet, basename='book')

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
]
urlpatterns += router.urls
