from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student


@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:

        full_name = instance.first_name + ' ' + instance.last_name
        print(instance.first_name, instance.last_name)
        Student.objects.create(full_name=full_name, user=instance)
