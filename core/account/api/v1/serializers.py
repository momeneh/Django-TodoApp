from rest_framework import serializers
from ...models import User
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model


class Registrationerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(max_length = 255,write_only = True,required=True)
    
    class Meta:
        model = User
        fields = ['email','password','password_confirmation']
        
    
    def validate(self,attrs):
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({'password': 'passwords dont match'})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError  as e:
            raise serializers.ValidationError({'password':list(e.messages)}) 
        return super().validate(attrs)
    
    def create(self,validated_data):
        validated_data.pop('password_confirmation',None)
        return User.objects.create_user(**validated_data)
    

class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )
    
    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError({'detail':msg}, code='authorization')
            if not user.is_verified:
                raise serializers.ValidationError({'detail':'user is not verified'}, code='authorization')

        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    

class ChangePasswordSerializer(serializers.Serializer):
    model = get_user_model()

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"details": "Passwords do not match"}
            )
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError  as e:
            raise serializers.ValidationError({'password':list(e.messages)}) 
    
        return super().validate(attrs)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data    
    


class GetUserForEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)
    def validate(self, attrs):
        email = attrs.get('email')
        try :
            user = User.objects.get(email = email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'detail':'could not find user with this email'})

        
        attrs['user'] = user    
        return super().validate(attrs)
    

class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
    token = serializers.CharField(read_only=True)
    
    def set_value(self, dictionary, keys, value):
        return super().set_value( dictionary, keys, value)
    
    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"details": "Passwords do not match"}
            )
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError  as e:
            raise serializers.ValidationError({'password':list(e.messages)}) 
    
        return super().validate(attrs)
