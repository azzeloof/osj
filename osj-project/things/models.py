from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager
from hitcount.models import HitCountMixin, HitCount
from django_bleach.models import BleachField
from .validators import validateFileSize, validateNumberOfFiles
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify
from reports.models import Report

class Thing(models.Model):
    def __str__(self):
        return self.title

    @property
    def totalLikes(self):
        return self.likes.count() 

    # Model to handle things
    title = models.CharField(max_length=128)
    tagline = BleachField(max_length=1024, blank=True)
    description = BleachField(max_length=8096)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    licence = models.ForeignKey("Licence", on_delete=models.PROTECT)
    category = models.ForeignKey("Category", null=True, on_delete=models.SET_NULL)
    tags = TaggableManager()
    #tags = TagField(verbose_name="tags", null=True)
    repo = models.URLField(max_length=256, blank=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    # hitcounts: https://dev.to/thepylot/how-to-track-number-of-hits-views-for-chosen-objects-in-django-django-packages-series-2-3bcb
    hitcount_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hitcount_generic_relation')
    featured = models.BooleanField(default=False)
    date_featured = models.DateTimeField(null=True)
    reports = GenericRelation(Report)


class Image(models.Model):
    # Model to handle images
    # Based on a solution found at:
    # https://medium.com/ibisdev/upload-multiple-images-to-a-model-with-django-fd00d8551a1c
    alt = models.CharField(max_length=256, blank=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='image_set')
    image = models.ImageField(upload_to='images/')
    featured = models.BooleanField(default=False)
    order = models.IntegerField()#default=0)

    class Meta:
        ordering = ('order',)


class File(models.Model):
    # Model to handle files attached to things
    # Based on Image model
    name = models.CharField(max_length=256, blank=True)
    thing = models.ForeignKey(Thing, on_delete=models.CASCADE, related_name='file_set', validators=[validateNumberOfFiles])
    file = models.FileField(upload_to='files', validators=[validateFileSize])
    default = models.BooleanField(default=False)
    downloads = models.IntegerField(default=0)
    order = models.IntegerField()#default=0)

    class Meta:
        ordering = ('order',)


class SuperCategory(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=256)


class Category(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(SuperCategory, on_delete=models.SET_NULL, null=True, blank=True)


class Licence(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(max_length=256)
    url = models.URLField(max_length=256, blank=True)
    html = models.TextField(max_length=1024)

