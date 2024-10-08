import os
from celery import shared_task
from icecream import ic
from .models import Book, logger
from .firebase_storage import upload_to_firebase


@shared_task(bind=True)
def upload_files_to_firebase(self, file_field, file_type, isbn, folder='audiobooks', subfolder=None):
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

        # Return the URL or a success message
        return f"Uploaded {file_type} for ISBN {isbn}: {book.poster_url or book.cover_url or book.ebook_url}"

    except Book.DoesNotExist:
        self.update_state(state='FAILURE', meta={'error': 'Book not found'})
        return None
    except Exception as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        return None

