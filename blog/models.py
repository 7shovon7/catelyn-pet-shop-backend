import uuid
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class BlogPost(models.Model):
    title = models.CharField(max_length=255, unique=True)
    title_en = models.CharField(max_length=255, unique=True, blank=True)
    slug = models.CharField(max_length=255, unique=True, blank=True)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def formatted_markdown(self):
        return markdownify(self.content)
    
    def save(self, *args, **kwargs):
        if not self.title_en:
            self.title_en = str(uuid.uuid4())
        if not self.slug:
            self.slug = slugify(self.title_en)
            # if BlogPost.objects.filter(slug=self.slug).exists():
            #     counter = 1
            #     original_slug = self.slug
            #     while BlogPost.objects.filter(slug=self.slug).exists():
            #         self.slug = f'{original_slug}-{counter}'
            #         counter += 1
        super(BlogPost, self).save(*args, **kwargs)
