# Generated by Django 4.1.7 on 2023-03-30 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0004_alter_student_date_of_birth_alter_student_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, to='MainSite.skill'),
        ),
    ]