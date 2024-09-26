from django.contrib import admin
from .models import Category

class UserCategories(admin.ModelAdmin):
    list_display = ('name',)  # Assuming 'name' is a field in Category

admin.site.register(Category, UserCategories)

