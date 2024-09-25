from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.category.models import Category
from apps.user.validators import validate_image


class User(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/avatar_default.png',
                              validators=[validate_image],
                              help_text='Upload an avatar image. If not provided, a default image will be used.')
    full_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    categories = models.ManyToManyField(Category, related_name='users')
    remember_me = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
