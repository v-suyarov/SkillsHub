# Generated by Django 4.2 on 2023-04-20 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0006_alter_student_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='Media/static/image'),
        ),
    ]