# Generated by Django 5.0.6 on 2024-06-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_alter_blogpost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
