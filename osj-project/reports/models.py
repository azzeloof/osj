from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from notifications.signals import notify


class Report(models.Model):
    def __str__(self):
        return self.description[0:20] + "..."
    reporter = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    date_reported = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    description = models.TextField(max_length=500)

    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]


@receiver(post_save, sender=Report)
def notify_superuser_of_report(sender, instance, created, **kwargs):
    if created:
        superusers = User.objects.filter(is_superuser=True)
        verb = "User content reported"
        description = instance.description
        notify.send(sender=instance, recipient=superusers, verb=verb, description=description)
