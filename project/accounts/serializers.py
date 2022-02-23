from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating user account."""

    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password',
            'email', 'first_name', 'last_name'
            )
        read_only_fields = ('id',)

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("Email not unique")
        return norm_email

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializes user data."""

    class Meta:
        model = User
        fields = ('url', 'username', 'email')
