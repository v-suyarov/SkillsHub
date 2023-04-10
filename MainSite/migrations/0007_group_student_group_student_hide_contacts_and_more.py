# Generated by Django 4.1.8 on 2023-04-10 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MainSite', '0006_alter_student_skills'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='group_students', to='MainSite.student'),
        ),
        migrations.AddField(
            model_name='student',
            name='hide_contacts',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='student',
            name='record_book',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='telegram',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_admission',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='Media/static/image'),
        ),
    ]