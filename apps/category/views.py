from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from icecream import ic
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.category import serializers
from apps.category.models import Category


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryListSerializer
    search_fields = ['name']

    def get_queryset(self):
        genres = cache.get('genres')
        ic(genres)
        if genres is None:
            genres = Category.objects.all()  # noqa
            serializer = self.serializer_class(genres, many=True)
            cache.set('genres', serializer.data)  # Store serialized data in cache
            return genres
        else:
            # Create a list of Category objects from the cached data
            genres = [Category(**item) for item in genres]
            # Use the Django model manager to create a queryset from the list
            return Category.objects.filter(id__in=[category.id for category in genres])  # noqa

    @extend_schema(operation_id='listCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryDetailSerializer

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = cache.get(f'category_{pk}')
        if obj is None:
            obj = super().get_object()
            serializer = self.serializer_class(obj)
            cache.set(f'category_{pk}', serializer.data)  # Store serialized data in cache
            return obj
        else:
            obj = Category(**obj)  # Convert cached data back to Category object
            return obj

    @extend_schema(operation_id='retrieveCategory', tags=['Category'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryCreateSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='createCategory', tags=['Category'])
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Invalidate the list cache when a new category is created
            cache.delete('genres')
        return response


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryUpdateSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='putCategory', tags=['Category'])
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('genres')
            pk = kwargs.get('pk')
            cache.delete(f'category_{pk}')
        return response

    @extend_schema(operation_id='patchCategory', tags=['Category'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('genres')
            pk = kwargs.get('pk')
            cache.delete(f'category_{pk}')
        return response


class CategoryDeleteAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()  # noqa
    serializer_class = serializers.CategoryDetailSerializer
    permission_classes = (IsAdminUser,)

    @extend_schema(operation_id='deleteCategory', tags=['Category'])
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        # Invalidate the list and detail cache when a category is deleted
        cache.delete('genres')
        cache.delete(f'category_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)
