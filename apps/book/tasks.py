import os
from celery import shared_task
from icecream import ic

from .models import Book
from .firebase_storage import upload_to_firebase


@shared_task
def upload_files_to_firebase(file_field, file_type, isbn, folder='audiobooks', subfolder=None):
    ic(file_field)
    ic(file_type)
    ic(isbn)

    try:
        book = Book.objects.get(isbn=isbn)
        file_name = os.path.basename(file_field)

        if file_type == 'poster':
            book.poster_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)
        elif file_type == 'cover':
            book.cover_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)
        elif file_type == 'ebook':
            book.ebook_url = upload_to_firebase(file_field, file_name, folder=folder, subfolder=subfolder)

        book.save()

    except Book.DoesNotExist:
        ic(f"Book with ISBN {isbn} not found.")
    except Exception as e:
        ic(f"Error uploading file to Firebase: {str(e)}")
