# blog/admin.py

from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import BlogPost

admin.site.register(BlogPost, MarkdownxModelAdmin)
