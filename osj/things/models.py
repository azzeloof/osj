from django.db import models
from django.contrib.auth.models import User

class Thing(models.Model):
    def __str__(self):
        return self.title

    # Model to handle things
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    #licence = 
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)
    repo = models.URLField(max_length=200, blank=True)


class Image(models.Model):
    # Model to handle images
    # Based on a solution found at:
    # https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c
    alt = models.CharField(max_length=255, blank=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='image_set')
    image = models.ImageField(upload_to='images/')
    featured = models.BooleanField(default=False)


class File(models.Model):
    # Model to handle files attached to things
    # Based on Image model
    name = models.CharField(max_length=255, blank=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='file_set')
    file = models.FileField(upload_to='files')
    default = models.BooleanField(default=False)


class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=127)


