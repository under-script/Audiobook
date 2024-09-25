from django.contrib.auth import get_user_model
from django.core.cache import cache
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

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
