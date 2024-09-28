from datetime import timedelta

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.text import slugify
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import ReadOnlyField
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import UserCategory

User = get_user_model()


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'image']


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=20, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password2')
        if password != password2:
            raise serializers.ValidationError('Password1 does not match Password2')
        return attrs

    def create(self, data):
        user = User(
            email=data['email'],
            username=data['username']
        )
        user.set_password(data['password'])
        user.is_active = False
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    old_password_again = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, attrs):
        user = self.context['request'].user

        old_password = attrs.get('old_password')
        old_password_again = attrs.get('old_password_again')

        # Validate both old_password and old_password_again
        if old_password != old_password_again:
            raise serializers.ValidationError({"old_password_again": "Old passwords do not match"})

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})

        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "realname",
            "phone",
            "image",
            "location",
            "bio"
        )

    def update(self, instance, validated_data):
        if "image" not in validated_data or not validated_data["image"]:
            validated_data["image"] = instance.image
        return super().update(instance, validated_data)


class CustomTokenCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate user based on email and password
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        # Ensure that the user is not AnonymousUser and is properly authenticated
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication failed")

        refresh = RefreshToken.for_user(user)
        remember_me = attrs.get('remember_me')

        if remember_me:
            refresh.set_exp(lifetime=timedelta(days=30))
        else:
            refresh.set_exp(lifetime=timedelta(days=7))

        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'remember_me': remember_me
        }

        return data

class UserCategoryListSerializer(serializers.ModelSerializer):
    category_name = ReadOnlyField(source="category.name")
    class Meta:
        model = UserCategory
        fields = ["id", "category", "category_name"]


class UserCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = '__all__'


class UserCategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ["id", 'category']
        read_only_fields = ["id"]


class UserCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = ["id", 'category']
        read_only_fields = ["id"]

class CustomUserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'username', 'email', 'phone', 'birth_date', 'image']


class CustomUserCreateSerializer(UserCreateSerializer, CustomUserBaseSerializer):
    class Meta(CustomUserBaseSerializer.Meta, UserCreateSerializer.Meta):
        fields = CustomUserBaseSerializer.Meta.fields + ['password']


class CustomUserSerializer(UserSerializer, CustomUserBaseSerializer):
    class Meta(CustomUserBaseSerializer.Meta, UserSerializer.Meta):
        fields = CustomUserBaseSerializer.Meta.fields

