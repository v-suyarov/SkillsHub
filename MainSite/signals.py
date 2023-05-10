
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, CustomUser
import os
import random

@receiver(post_save, sender=CustomUser)
def create_student(sender, instance, created, **kwargs):
    if created:
        full_name = instance.first_name + ' ' + instance.last_name
        student = Student.objects.create(full_name=full_name, user=instance, record_book=instance.username)
        image_folder = 'Media/static/image/default'
        if os.path.exists(image_folder):
            images = os.listdir(image_folder)
            if images:
                image_name = random.choice(images)
                image_path = os.path.join(image_folder, image_name)
                student.photo.save(image_name, open(image_path, 'rb'), save=True)
                print("Случайное фото назначено")
        else:
            print("Папка не найдена")
