from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Based on solution at https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html

class Profile(models.Model):
    def __str__(self):
        return self.user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to='uploads/profile_photos')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()