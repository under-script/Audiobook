from django.contrib import admin

from apps.base.models import Author, Narrator, Book, Audiobook, Review, Bookmark

# Register your models here.
admin.site.register([Author, Narrator, Book, Audiobook, Review, Bookmark])
