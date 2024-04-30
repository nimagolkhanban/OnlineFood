import os

from django.core.exceptions import ValidationError


def allow_image_only(value):
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    # tip : allways remember the value.name because the  value itself does not word properly
    ext = os.path.splitext(value.name)[1]
    if ext.lower() not in allowed_extensions:
        raise ValidationError(f'The file format is not acceptable. Please upload {str(allowed_extensions)}')
