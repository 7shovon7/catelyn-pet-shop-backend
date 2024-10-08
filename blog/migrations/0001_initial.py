# Generated by Django 5.0.6 on 2024-08-06 19:33

import markdownx.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
                ('title_en', models.CharField(blank=True, max_length=255, unique=True)),
                ('slug', models.CharField(blank=True, max_length=255, unique=True)),
                ('featured_image', models.CharField(blank=True, max_length=255, null=True)),
                ('content', markdownx.models.MarkdownxField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
