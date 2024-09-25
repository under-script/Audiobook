from django.core.exceptions import ValidationError


def validate_image(image):
    file_size = image.file.size
    limit_kb = 500
    if file_size > limit_kb * 1024:
        raise ValidationError(f"Max size of file is {limit_kb} KB")
