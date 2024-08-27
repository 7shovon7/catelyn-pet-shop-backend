# # from django.conf import settings
# from django.contrib.auth import get_user_model
# from rest_framework import permissions, status
# from rest_framework.mixins import (
#     CreateModelMixin,
#     ListModelMixin,
#     RetrieveModelMixin,
#     UpdateModelMixin,
# )
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet

# from .serializers import (
#     UserSerializer,
# )


# class UserViewSet(
#     ListModelMixin,
#     CreateModelMixin,
#     RetrieveModelMixin,
#     UpdateModelMixin,
#     GenericViewSet,
# ):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
    
#     def get_queryset(self):
#         user_id = self.request.user.id
#         queryset = get_user_model().objects.filter(id=user_id).first()
#         if hasattr(queryset, 'manager'):
#             self.serializer_class = ProductManagerSerializer
#             queryset = queryset.manager
#         elif hasattr(queryset, 'customer'):
#             self.serializer_class = CustomerSerializer
#             queryset = queryset.customer
#         else:
#             queryset = None
#         return queryset
    
#     def list(self, request):
#         queryset = self.get_queryset()
#         serializer = self.serializer_class(queryset, many=False)
#         return Response(serializer.data)
    
#     def create(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if queryset is None:
#             return Response(status=status.HTTP_403_FORBIDDEN, data={"details": "Profile creation should be done at the signup stage"})
#         else:
#             serializer = self.get_serializer(queryset, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)
        