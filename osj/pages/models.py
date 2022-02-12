from django.db import models

# Create your models here.

class Page(models.Model):
    title = models.CharField(max_length=127)
    content = models.TextField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=127)
    