import os
from firebase_admin import storage

def upload_to_firebase(file, file_name):
    # Get the storage bucket
    bucket = storage.bucket()
    # Create a blob (file object) in the bucket
    blob = bucket.blob(file_name)
    # Upload the file to Firebase Storage
    blob.upload_from_file(file)

    # Make the file publicly accessible (optional)
    blob.make_public()

    # Return the public URL
    return blob.public_url
