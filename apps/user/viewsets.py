from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
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

