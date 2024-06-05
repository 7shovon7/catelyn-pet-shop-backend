# Generated by Django 5.0.6 on 2024-06-04 07:20

from django.db import migrations
import uuid


def populate_title_field(apps, schema_editor):
    BlogPost = apps.get_model('blog', 'BlogPost')
    for post in BlogPost.objects.all():
        post.title = post.temp_title
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_blogpost_title'),
    ]

    operations = [
        migrations.RunPython(populate_title_field)
    ]
