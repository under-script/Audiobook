from django.contrib.auth import get_user_model
from django.db import models

from apps.base.TimeStampModel import TimeStampModel
from apps.category.models import Category

User = get_user_model()


class Author(TimeStampModel):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Narrator(TimeStampModel):
    name = models.CharField(max_length=255)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Book(TimeStampModel):
    title = models.CharField(max_length=255)
    summary = models.TextField()
    categories = models.ManyToManyField(Category, related_name='ebooks')
    author = models.ForeignKey(Author, related_name='ebooks', on_delete=models.CASCADE)
    publication_date = models.DateField()

    isbn = models.CharField(max_length=13, unique=True)
    page_count = models.PositiveSmallIntegerField()
    # language = models.IntegerField(choices=LANGUAGE_CODE, default=LANGUAGE_CODE)
    file_url = models.FileField(upload_to='ebooks/')  # Book file (e.g., PDF, EPUB)
    image = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title


class Audiobook(TimeStampModel):
    ebook = models.ForeignKey(Book, related_name='audiobooks', on_delete=models.CASCADE)  # Relation to Book
    publication_date = models.DateField()
    narrator = models.ForeignKey(Narrator, related_name='audiobooks', on_delete=models.CASCADE)
    duration = models.DurationField()
    audio_file_url = models.FileField(upload_to='audiobooks/')  # Audiobook file (e.g., MP3)

    def __str__(self):
        return self.ebook.title


class Review(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    audiobook = models.ForeignKey(Audiobook, related_name='reviews', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.FloatField()
    comment = models.TextField()

    def __str__(self):
        return f'Review by {self.user.username}'  # noqa


class Bookmark(TimeStampModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='bookmarks', on_delete=models.CASCADE, null=True, blank=True)
    time = models.IntegerField(null=True, blank=True)
