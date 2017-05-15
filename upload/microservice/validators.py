import magic
from django.conf import settings
from django.core.exceptions import ValidationError

def validate_file_type(field):
    file_type = magic.from_buffer(field.file.read(1024), mime=True)

    if file_type not in settings.UPLOAD_FILE_TYPES.get("images") and file_type not in settings.UPLOAD_FILE_TYPES.get("videos"):
        raise ValidationError('File type not supported. JPEG, PNG, or MP4 recommended.')