from rest_framework.pagination import LimitOffsetPagination


class BlogPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
