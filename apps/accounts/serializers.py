from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Company

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    class Meta:
        model = User
        fields = (
            'url',
            'id',
            'username',
            'password'
        )

        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
            return  User.objects.create_user(**validated_data)

        def update(self, instance, validated_data):
            updated = super().update(instance, validated_data)

            if 'password' in validated_data:
                updated.set_password(validated_data['password'])
                updated.is_active = True
                updated.save()

            return updated


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = (
            'id',
            'name',
            'address'
        )


class AccountSerializer(serializers.Serializer):
    company = CompanySerializer()
    user = UserSerializer()

    def create(self, validated_data):
        company_data = validated_data['company']
        user_data = validated_data['user']

        company, user = Company.objects.create_account(
            company_name=company_data.get('name'),
            company_address=company_data.get('address'),
            username=user_data.get('username'),
            password=user_data.get('password')
        )
        return {'company': company, 'user': user}

    def update(self, instance, validated_data):
        raise NotImplementedError('Cannot call update on an account')
