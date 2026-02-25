from rest_framework import generics
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from ...models import User
from django.template.loader import render_to_string
from .utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import jwt
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from premailer import transform
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from datetime import timedelta


def get_tokens_for_user(user):
    token = RefreshToken.for_user(user)
    access = token.access_token
    access.set_exp(lifetime=timedelta(minutes=15))
    return str(access)


class Registration(generics.GenericAPIView):
    serializer_class = Registrationerializer

    def post(self, request, *arg, **kwargs):
        serializer = Registrationerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email = user.email
        token = get_tokens_for_user(user)
        html_template = render_to_string(
            "emails/activation.tpl", {"token": token, "user": user}
        )
        html_inlined = transform(html_template)
        message = EmailMultiAlternatives(
            "Activation Mail", html_inlined, "from@example.cpm", [email]
        )
        message.attach_alternative(html_inlined, "text/html")
        EmailThread(message).start()
        return Response(
            {
                "detail": "Registration succeeded ,activation link has been sent to the email"
            },
            status=status.HTTP_200_OK,
        )


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class DiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response("token removed", status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.GenericAPIView):
    """
    An endpoint for changing password.
    """

    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("password"))
            self.object.save()
            response = {
                "details": "Password updated successfully",
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivationApiView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"detail": "token has been expierd"}, status=status.HTTP_400_BAD_REQUEST
            )
        except InvalidSignatureError:
            return Response(
                {"detail": "token is not valid"}, status=status.HTTP_400_BAD_REQUEST
            )
        except DecodeError:
            return Response(
                {"detail": "token has a problem"}, status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(pk=user_id)
        if user.is_verified:
            return Response(
                {"detail": "your account has been verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.is_verified = True
        user.save()
        return Response(
            {"detail": "your account has been verified successfully"},
            status=status.HTTP_200_OK,
        )


class ActivationResendApiView(generics.GenericAPIView):
    serializer_class = GetUserForEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = GetUserForEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if user.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is already activated and verified"}
            )
        token = get_tokens_for_user(user)
        html_template = render_to_string(
            "emails/activation.tpl", {"token": token, "user": user}
        )
        html_inlined = transform(html_template)
        message = EmailMultiAlternatives(
            "Activation Mail", html_inlined, "from@example.cpm", [user.email]
        )
        message.attach_alternative(html_inlined, "text/html")
        EmailThread(message).start()
        return Response(
            {"detail": "activation link has been sent to the email"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(generics.GenericAPIView):
    """
    resetting password
    """

    serializer_class = GetUserForEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = GetUserForEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        token = get_tokens_for_user(user)
        reset_path = reverse(
            "account:api-v1:reset-password-confirm", kwargs={"token": token}
        )
        reset_url = request.build_absolute_uri(reset_path)

        html_template = render_to_string(
            "emails/reset_password.tpl",
            {
                "user": user,
                "reset_url": reset_url,
            },
        )
        html_inlined = transform(html_template)
        message = EmailMultiAlternatives(
            "Reset Password", html_inlined, "from@example.cpm", [user.email]
        )
        message.attach_alternative(html_inlined, "text/html")
        EmailThread(message).start()
        return Response(
            {"detail": "Reset Password link has been sent to the email"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordConfirmView(generics.GenericAPIView):
    """
    resetting password Confirm
    """

    serializer_class = PasswordResetConfirmSerializer

    def get(self, request, token, *args, **kwargs):
        """
        checking token and let the user fill new password
        """
        self.check_token(token)
        return Response({"detail": "enter new password"}, status=status.HTTP_200_OK)

    def put(self, request, token, *args, **kwargs):
        """
        check passwords and change password
        """
        self.user = User.objects.get(pk=self.check_token(token))

        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.user.set_password(serializer.data.get("password"))
        self.user.save()

        return Response(
            {"detail": "Password updated successfully"}, status=status.HTTP_200_OK
        )

    def check_token(self, token):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get("user_id")
        except ExpiredSignatureError:
            raise serializers.ValidationError({"token": "token has been expierd"})
        except InvalidSignatureError:
            raise serializers.ValidationError({"token": "token is not valid"})
        except DecodeError:
            raise serializers.ValidationError({"token": "token has a problem"})

        return user_id
