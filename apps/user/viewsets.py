from djoser.views import UserViewSet
from rest_framework.decorators import action

from apps.user import serializers


class CustomUserViewSet(UserViewSet):
    serializer_class = serializers.UserSerializer
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance # noqa
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)