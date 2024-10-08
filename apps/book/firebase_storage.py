import mimetypes
from firebase_admin import storage

def upload_to_firebase(file_path, file_name, folder='others', subfolder=None):
    # Get the storage bucket
    bucket = storage.bucket()

    # Construct the full path for the file
    if subfolder:
        full_path = f"{folder}/{subfolder}/{file_name}"
    else:
        full_path = f"{folder}/{file_name}"

    # Determine the content type based on the file extension
    content_type, _ = mimetypes.guess_type(file_path)

    # Create a blob (file object) in the bucket
    blob = bucket.blob(full_path)

    # Open the file and upload it to Firebase Storage
    with open(file_path, 'rb') as file:
        blob.upload_from_file(file, content_type=content_type)

    # Make the file publicly accessible (optional)
    blob.make_public()

    # Return the public URL
    return blob.public_url
