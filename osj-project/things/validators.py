from django.core.exceptions import ValidationError
from osj.settings import MAX_FILE_SIZE, MAX_N_FILES
import things.models

def validateFileSize(uploadedFile):
    try:
        filesize = uploadedFile.size
    except:
        filesize = 0
    if filesize > MAX_FILE_SIZE:
        maxSize = str(int(MAX_FILE_SIZE/(1024**2))) + "MB"
        raise ValidationError("The maximum file size is " + maxSize)
    else:
        return uploadedFile

def validateNumberOfFiles(thing):
    if File.objects.filter(thing_id=thing).count() >= MAX_N_FILES:
        raise ValidationError("Too many files! Only " + str(MAX_N_FILES) + " are allowed.")
    #try:
    #    nFiles = len(thing.thing_set.all()) + 1
    #except:
    #    nFiles = 0
    #if nFiles > MAX_N_FILES:
    #    raise ValidationError("Too many files! Only " + str(MAX_N_FILES) + " are allowed.")
    #else:
    #    return thing

