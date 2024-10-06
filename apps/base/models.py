from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.category.models import Category


class Author(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


def get_chapter_audio_upload_path(instance, filename):
    # Use the ISBN of the related book for the audio file's path
    return f'audios/{instance.book.isbn}/{filename}'


def get_ebook_upload_path(instance, filename):
    # Use the title of the book for the ebook file's path
    return f'books/{instance.title}/{filename}'


class Chapter(TimeStampedModel):
    chapterId = models.AutoField(primary_key=True)
    chapterName = models.CharField(max_length=255)
    audio = models.FileField(upload_to=get_chapter_audio_upload_path)  # Dynamic upload path

    # Assuming a foreign key to link chapters to a specific book
    book = models.ForeignKey('Book', related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return self.chapterName


class Book(TimeStampedModel):
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    cover = models.ImageField(upload_to='covers/', null=True, blank=True)
    title = models.CharField(max_length=255, unique=True)
    author = models.ForeignKey('Author', related_name='books', on_delete=models.CASCADE)
    rate = models.FloatField(
        validators=[MinValueValidator(0.1), MaxValueValidator(5.0)]
    )
    categories = models.ManyToManyField(Category, related_name='books')
    summary = models.TextField(max_length=3000, unique=True)
    full_audio = models.FileField(null=True, blank=True)
    ebook = models.FileField(upload_to=get_ebook_upload_path)  # Dynamic upload path
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def __str__(self):
        return self.title
