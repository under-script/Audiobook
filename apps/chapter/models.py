from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.book.models import Book


def get_chapter_audio_upload_path(instance, filename):
    # Use the ISBN of the related book for the audio file's path
    return f'audios/{instance.book.isbn}/{filename}'


class Chapter(TimeStampedModel):
    chapterId = models.AutoField(primary_key=True)
    chapterName = models.CharField(max_length=255)
    audio = models.FileField(upload_to=get_chapter_audio_upload_path)  # Dynamic upload path

    # Assuming a foreign key to link chapters to a specific book
    book = models.ForeignKey(Book, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return self.chapterName
