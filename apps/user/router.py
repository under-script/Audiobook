from rest_framework.routers import DefaultRouter

from apps.user.viewsets import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
urlpatterns = router.urls