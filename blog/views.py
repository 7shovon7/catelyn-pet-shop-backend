# blog/views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import BlogPost
from .paginations import BlogPagination
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = BlogPagination
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        lookup_field_value = self.kwargs[self.lookup_field]
        
        try:
            obj = get_object_or_404(BlogPost, id=lookup_field_value)
        except:
            obj = get_object_or_404(BlogPost, slug=lookup_field_value)
            
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
    
    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]
        obj = get_object_or_404(BlogPost, id=lookup_field_value)
        return obj
    
    def get_object_by_slug(self, slug):
        return get_object_or_404(BlogPost, slug=slug)
