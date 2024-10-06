from django.contrib import admin
from apps.base.models import Author, Book, Chapter


# Register your models here.
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 10

    class Meta:
        abstract = True


class AuthorAdmin(BaseAdmin):
    list_display = [f.name for f in Author._meta.fields]


class BookAdmin(BaseAdmin):
    list_display = [f.name for f in Book._meta.fields]


class ChapterAdmin(BaseAdmin):
    list_display = [f.name for f in Chapter._meta.fields]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BaseAdmin)
admin.site.register(Chapter, ChapterAdmin)
