from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.base.TimeStampModel import TimeStampModel
from apps.category.models import Category
from apps.user.validators import validate_image


class User(AbstractUser):
    password = models.CharField(max_length=128, null=True, blank=True)
    username = models.CharField(max_length=20, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=9, null=True, blank=True)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/avatar_default.png',
                              validators=[validate_image],
                              help_text='Upload an avatar image. If not provided, a default image will be used.')
    full_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='users', blank=True)
    remember_me = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserCategory(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

    # def __str__(self):
    #     return f"{self.user} - {self.category}"

#
# class UserProfile(TimeStampModel):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     categories = models.ManyToManyField(Category, through='UserCategory')
