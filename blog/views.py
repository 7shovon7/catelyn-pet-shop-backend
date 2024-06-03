# blog/views.py

from rest_framework import viewsets
from .models import BlogPost
from .paginations import BlogPagination
from .serializers import BlogPostSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    pagination_class = BlogPagination
