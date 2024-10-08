from django.db import models
from django_extensions.db.models import TimeStampedModel

from apps.book.models import Book


def get_chapter_audio_upload_path(instance, filename):
    # Use the ISBN of the related book for the audio file's upload path
    return f'audiobooks/{instance.book.isbn}/chapters/{filename}'

class Chapter(TimeStampedModel):
    chapterId = models.AutoField(primary_key=True)
    audio = models.FileField(upload_to=get_chapter_audio_upload_path)  # Use FileField to upload audio files

    # Foreign key to link chapters to a specific book using a string reference
    book = models.ForeignKey(Book, related_name='chapters', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.book.title} - Chapter {self.chapterId}"
