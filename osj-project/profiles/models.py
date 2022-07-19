from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_bleach.models import BleachField
from notifications.signals import notify
from django_email_verification import send_email
from django.contrib.contenttypes.fields import GenericRelation
from reports.models import Report

# Based on solution at https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

class Profile(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    description = BleachField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='profile_photos', blank=True)
    email_verified = models.BooleanField(default=False)
    reports = GenericRelation(Report)


def sendVerificationEmail():
    pass


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance, slug=instance.username)
        # Send welcome notification
        notificationSender = User.objects.get(username="adam")
        recipient = instance
        verb = "Welcome to OpenJewelry!"
        description = "Thank you for joining the OpenJewelry commnuity! We're glad to have you here."
        notify.send(sender=notificationSender, recipient=recipient, verb=verb, description=description)
        # Send verification email
        profile.email_verified = False
        profile.save()
        send_email(instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()