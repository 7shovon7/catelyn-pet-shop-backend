from django.contrib import admin
from .models import Category, CustomField


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']


@admin.register(CustomField)
class CustomFieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'key', 'is_required', 'is_private']
    search_fields = ['name', 'key']
    readonly_fields = ['id', 'key']

    fieldsets = [
        ("Basic Information", {"fields": ['id', 'name', 'is_required', 'is_private']}),
        ("Advanced Settings", {"fields": ['key'], 'classes': ['collapse']}),
    ]
