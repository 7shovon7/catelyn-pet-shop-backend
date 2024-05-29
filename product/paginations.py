from rest_framework.pagination import LimitOffsetPagination


class ProductPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ReviewPagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20
