from users.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        extra_kwargs = {'first_name': {'required': True},
                        'last_name': {'required': True}, }

    def validate_password(self, value):
        """
        Validate password using Django's password validators
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user is None:
            raise serializers.ValidationError(_("User does not exist"))

        if not user.check_password(data['password']):
            raise serializers.ValidationError(_("Incorrect email or password"))

        return {'user': user}

    def to_representation(self, instance):
        return super().to_representation(instance)
