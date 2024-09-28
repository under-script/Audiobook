from djoser.views import UserViewSet

from apps.user import serializers


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == 'me':
            return serializers.CustomUserSerializer
        return super().get_serializer_class()