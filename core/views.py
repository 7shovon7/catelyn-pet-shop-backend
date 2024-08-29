from rest_framework import permissions, status, generics
from rest_framework.response import Response

# from .models import User
from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, UserCreateSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Include tokens in the response
        tokens = serializer.get_tokens(user)
        return Response({
            **tokens,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "user_role": user.user_role,
            },
        }, status=status.HTTP_201_CREATED)

# class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserDetailSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # def settings(self, request):
#     #     user = self.request.user
#     #     serializer = self.get_serializer(user)
#     #     return Response(serializer.data)

#     def list(self, request):
#         user = request.user
#         serializer = self.get_serializer(user)
#         return Response(serializer.data)
    
#     def create(self, request, *args, **kwargs):
#         user = self.request.user
#         serializer = UserPartialUpdateSerializer(user, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)

    # def update_settings(self, request):
    #     user = self.request.user
    #     serializer = UserPartialUpdateSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=400)
    
    
class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password reset code has been sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    
    
# class UserViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserDetailSerializer

#     def get_queryset(self):
#         requested_user_id = self.request.GET.get('id')
#         if requested_user_id is not None:
#             user_id = requested_user_id
#         else:
#             user_id = self.request.user.id
#         # Fetch the user profile
#         queryset = get_user_model().objects.filter(id=user_id).first().profile
#         if hasattr(queryset, 'spacehost'):
#             self.serializer_class = SpaceHostSerializer
#             queryset = queryset.spacehost
#         elif hasattr(queryset, 'advertiser'):
#             self.serializer_class = AdvertiserSerializer
#             queryset = queryset.advertiser
#         else:
#             queryset = None
#         return queryset

#     def list(self, request):
#         queryset = self.get_queryset()
#         # serializer_class = self.get_serializer_class()
#         serializer = self.serializer_class(queryset, many=False)
#         return Response(serializer.data)
    
#     def create(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         if queryset is None:
#             return Response(status=status.HTTP_403_FORBIDDEN, data={"details": "Profile creation should have been done at the registration level. Seems like that was not done. Something went wrong."})
#         else:
#             serializer = self.get_serializer(queryset, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             return Response(serializer.data)




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
        