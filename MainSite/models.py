from django.db import models
from django.contrib.auth.models import User
class Skill(models.Model):
    name = models.CharField(max_length=50)
    parent_skill = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='child_skills')

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Student(models.Model):
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    user = models.OneToOneField(User, null=False, default=None, on_delete=models.CASCADE, related_name='student')
    photo = models.ImageField(upload_to='Media/static/image', blank=True, null=True)
    skills = models.ManyToManyField(Skill, default=list)
    telegram = models.CharField(max_length=255, default="", null=True, blank=True)
    year_of_admission = models.DateField(blank=True, null=True)
    group = models.ForeignKey('Group', null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='group_students')
    hide_contacts = models.BooleanField(default=True)
    record_book = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.full_name





