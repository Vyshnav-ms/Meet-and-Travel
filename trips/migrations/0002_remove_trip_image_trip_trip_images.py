# Generated by Django 5.1.6 on 2025-03-07 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='image',
        ),
        migrations.AddField(
            model_name='trip',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='image'),
        ),
    ]
