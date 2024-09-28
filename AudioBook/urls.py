"""
URL configuration for AudioBook project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from AudioBook import settings
from apps.user.views import confirm_email, home

urlpatterns = [
    path('', home, name='home'),  # Home view
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]

api_urls = [
    path('user/', include('apps.user.urls')),
    path('notification/', include('apps.notification.urls')),
    path('categories/', include('apps.category.urls')),
]

spectacular_urls = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

jwt_urls = [
    path("auth/confirm-email/<uid>/<token>", confirm_email, name='confirm_email'),
    # path('api-auth/', include('rest_framework.urls')),
    # Then include Djoser's URLs
    path('auth/', include('apps.user.router')),
    # path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    # Custom JWT endpoints first
    # path('auth/jwt/create/', CustomTokenCreateView.as_view(), name='jwt_create'),
    # path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    # path('auth/', include('djoser.urls.jwt')),
    # path('auth/', include('drf_social_oauth2.urls')),
    # path('auth/social/google/', SocialLoginView.as_view(), name='google_login'),
]

urlpatterns += api_urls
urlpatterns += spectacular_urls
urlpatterns += jwt_urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
