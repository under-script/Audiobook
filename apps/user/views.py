from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.http import urlsafe_base64_decode
from drf_spectacular.utils import extend_schema, OpenApiResponse
from icecream import ic
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .models import UserCategory
from .serializers import UserRegisterSerializer, ChangePasswordSerializer, UserSettingsSerializer, \
    CustomTokenCreateSerializer

User = get_user_model()


# usmonovsaokhiddin@gmail.com

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        return user


@api_view(['GET'])
def verify_code(request):
    user_id = request.GET.get('user_id')
    code = request.GET.get('code')

    if not user_id:
        return Response({"message": "User ID not provided!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"message": "User with this ID not found!"}, status=status.HTTP_404_NOT_FOUND)

    code_cache = cache.get(user_id)
    if code_cache is not None and code == code_cache:
        user.is_active = True
        user.save()
        return Response({"message": "User successfully logged in"}, status=status.HTTP_200_OK)

    return Response({"message": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


register = UserCreateAPIView.as_view()


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSettingsView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


user_settings = UserSettingsView.as_view()
change_password = ChangePasswordView.as_view()


class CustomTokenCreateView(TokenObtainPairView):
    serializer_class = CustomTokenCreateSerializer

    @extend_schema(
        responses={
            200: OpenApiResponse(
                description="Custom Token Response",
                examples={
                    'application/json': {
                        'refresh': 'refresh-token-example',
                        'access': 'access-token-example',
                        'user': {
                            'id': 1,
                            'username': 'uznext',
                            'email': 'uznext17@gmail.com',
                        },
                        'remember_me': False
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserCategoryListAPIView(generics.ListAPIView):
    queryset = UserCategory.objects.all()  # noqa
    serializer_class = serializers.UserCategoryListSerializer
    search_fields = ['name']

    def get_queryset(self):
        categories = cache.get('categories')
        ic(categories)
        if categories is None:
            categories = UserCategory.objects.all()  # noqa
            serializer = self.serializer_class(categories, many=True)
            cache.set('categories', serializer.data)  # Store serialized data in cache
            return categories
        else:
            # Create a list of UserCategory objects from the cached data
            categories = [UserCategory(**item) for item in categories]
            # Use the Django model manager to create a queryset from the list
            return UserCategory.objects.filter(id__in=[category.id for category in categories])  # noqa

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
            cache.delete('categories')
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
            cache.delete('categories')
            pk = kwargs.get('pk')
            cache.delete(f'category_{pk}')
        return response

    @extend_schema(operation_id='patchUserCategory', tags=['UserCategory'])
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            # Invalidate the list and detail cache when a category is updated
            cache.delete('categories')
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
        cache.delete('categories')
        cache.delete(f'category_{pk}')
        return Response(status=status.HTTP_204_NO_CONTENT)


def confirm_email(request, uid, token):
    try:
        # Decode the `uid` to get the user
        uid = urlsafe_base64_decode(uid).decode()
        user = get_object_or_404(User, pk=uid)

        # Check if the token is valid using Django's default token generator
        is_token_valid = default_token_generator.check_token(user, token)
        if not is_token_valid:
            raise ValidationError("Invalid token.")

        # If the token is valid, confirm the email
        user.is_active = True  # Adjust this field based on your model
        user.save()

        messages.success(request, "Email successfully confirmed!")

    except (User.DoesNotExist, ValidationError, ValueError, TypeError, OverflowError) as e:
        messages.error(request, "Invalid confirmation link.")

    # Redirect to the homepage
    return redirect("/")

def home(request):
    return render(request, 'index.html')