# Generated by Django 5.0.6 on 2024-06-04 06:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_add_title_eng_and_generate_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='title_eng',
            field=models.CharField(blank=True, default=datetime.datetime(2024, 6, 4, 6, 22, 59, 281380, tzinfo=datetime.timezone.utc), max_length=255, unique=True),
            preserve_default=False,
        ),
    ]
