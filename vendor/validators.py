import os

from django.core.exceptions import ValidationError


def allow_image_only(value):
    allowed_extensions = ['.png', '.jpg', '.jpeg']
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in allowed_extensions:
        raise ValidationError('the file format is not acceptable please upload' + str(allowed_extensions))