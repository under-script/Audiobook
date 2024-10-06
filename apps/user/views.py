from django.contrib.auth import get_user_model
from django.core.cache import cache
from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, OpenApiResponse
from icecream import ic
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .models import UserCategory
from .serializers import CustomTokenCreateSerializer

User = get_user_model()


class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer


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


class UserCategoryListAPIView(generics.ListAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryListSerializer
    search_fields = ['name']

    def get_queryset(self):
        genres = cache.get('genres')
        ic(genres)
        if genres is None:
            genres = UserCategory.objects.all()  # noqa
            serializer = self.serializer_class(genres, many=True)
            cache.set('genres', serializer.data)  # Store serialized data in cache
            return genres
        else:
            # Create a list of UserCategory objects from the cached data
            genres = [UserCategory(**item) for item in genres]
            # Use the Django model manager to create a queryset from the list
            return UserCategory.objects.filter(id__in=[category.id for category in genres])  # noqa

    @extend_schema(operation_id='listUserCategory', tags=['UserCategory'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryDetailSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'category_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'category_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = UserCategory(**obj)  # Convert cached data back to UserCategory object
            return obj

    @extend_schema(operation_id='retrieveUserCategory', tags=['UserCategory'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserCategoryCreateAPIView(generics.CreateAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryCreateSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='createUserCategory', tags=['UserCategory'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new category is created
            cache.delete('genres')
        return response


class UserCategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryUpdateSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='putUserCategory', tags=['UserCategory'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('genres')
            pk = kwargs.get('pk')
            cache.delete(f'category_{pk}')
        return response

    @extend_schema(operation_id='patchUserCategory', tags=['UserCategory'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('genres')
            pk = kwargs.get('pk')
            cache.delete(f'category_{pk}')
        return response


class UserCategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryDetailSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='deleteUserCategory', tags=['UserCategory'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a category is deleted
        cache.delete('genres')
        cache.delete(f'category_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)
