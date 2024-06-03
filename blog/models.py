from django.db import models
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = MarkdownxField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def formatted_markdown(self):
        return markdownify(self.content)
