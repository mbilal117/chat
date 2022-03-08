from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from . import serializers

User = get_user_model()

class AccountCreate(generics.CreateAPIView):
    name = 'account-create'
    serializer_class = serializers.AccountSerializer


class UserList(generics.ListCreateAPIView):
    name = 'user-list'
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        company_id = self.request.user.company_id
        serializer.save(company_id=company_id)

    def get_queryset(self):
        company_id = self.request.user.company_id
        return super(UserList, self).get_queryset().filter(company_id=company_id)


class CompanyDetail(generics.RetrieveUpdateAPIView):
    name = 'company-detail'
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.CompanySerializer

    def get_object(self):
        return self.request.user.company


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    name = 'user-detail'
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.UserSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        company_id = self.request.user.company_id
        return super(UserDetail, self).get_queryset().filter(company_id=company_id)