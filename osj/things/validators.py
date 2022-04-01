from django.core.exceptions import ValidationError

def validateFileSize(uploadedFile):
    try:
        filesize = uploadedFile.size
    except:
        filesize = 0

    if filesize > 5242880:
        raise ValidationError("The maximum file size is 50MB")
    else:
        return uploadedFile
