from django.db import models

# Create your models here.

class Page(models.Model):
    def __str__(self):
        return self.title
        
    title = models.CharField(max_length=127)
    content = models.TextField(max_length=20000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.CharField(max_length=127)
    