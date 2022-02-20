from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
