from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from icecream import ic
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import UserCategory
from .serializers import UserCategorySerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance  # noqa
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            ic(f"Image type: {type(image_file)}")
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Custom logic for deleting the user
        instance = self.get_object()

        # Check if the user is a superuser
        if request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)

            # Perform the deletion
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Return a permission denied response for non-superusers
        return Response(
            data={
                "detail": "You don't have permission to delete this profile."
            },
            status=status.HTTP_403_FORBIDDEN
        )


class UserCategoryViewSet(viewsets.ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer
