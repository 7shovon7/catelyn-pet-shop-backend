from django.db import migrations, models
from django.utils.text import slugify
import uuid


def populate_title_eng(apps, schema_editor):
    BlogPost = apps.get_model('blog', 'BlogPost')
    for post in BlogPost.objects.all():
        if not post.title_eng:
            post.title_eng = str(uuid.uuid4())
        post.save()


# def generate_unique_slugs(apps, schema_editor):
#     BlogPost = apps.get_model('blog', 'BlogPost')
    
#     for post in BlogPost.objects.all():
#         if not post.slug:
#             post.slug = slugify(post.title)
#             if BlogPost.objects.filter(slug=post.slug).exists():
#                 # Ensure the slug is unique by appending a counter if necessary
#                 counter = 1
#                 original_slug = post.slug
#                 while BlogPost.objects.filter(slug=post.slug).exists():
#                     post.slug = f'{original_slug}-{counter}'
#                     counter += 1
#             post.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='title_eng',
            field=models.CharField(max_length=255, blank=True, null=True),
        ),
        migrations.RunPython(populate_title_eng),
        # migrations.AddField(
        #     model_name='blogpost',
        #     name='slug',
        #     field=models.SlugField(max_length=255, unique=True, blank=True),
        # ),
        # migrations.RunPython(generate_unique_slugs),
    ]
