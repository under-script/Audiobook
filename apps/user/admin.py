from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from apps.user.models import UserCategory

User = get_user_model()


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_superuser', 'is_active', 'date_joined', 'get_avatar', 'full_name', 'phone', 'remember_me']

    def get_avatar(self, obj):
        if obj.image != 'avatar_default.png' and hasattr(obj.image, 'url'):
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return format_html('<img src="{}" width="50" height="50" />', '/media/avatars/avatar_default.png')

    get_avatar.short_description = 'Image'

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')


admin.site.register(User, UserAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)
