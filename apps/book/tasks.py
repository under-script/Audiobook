from celery import shared_task
from .models import Book
from .firebase_storage import upload_to_firebase

@shared_task
def upload_files_to_firebase(file_field, file_type, book_id):
    book = Book.objects.get(id=book_id)

    # Get the file path from the file field
    file_path = file_field.path

    if file_type == 'poster':
        book.poster_url = upload_to_firebase(file_path, f"{book_id}_poster", folder='posters')
    elif file_type == 'cover':
        book.cover_url = upload_to_firebase(file_path, f"{book_id}_cover", folder='covers')
    elif file_type == 'ebook':
        book.ebook_url = upload_to_firebase(file_path, f"{book_id}_ebook", folder='ebooks')

    # Save the updated book object
    book.save()
