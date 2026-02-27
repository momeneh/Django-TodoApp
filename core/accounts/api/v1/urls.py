from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import *

app_name = "api-v1"
urlpatterns = [
    # registration
    path("registration/", Registration.as_view(), name="registration"),
    # activation
    path(
        "activation/confirm/<str:token>", ActivationApiView.as_view(), name="activation"
    ),
    # resend activation
    path(
        "activation/resend/",
        ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    # change password
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # reset password
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path(
        "reset_password_confirm/<str:token>",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    # login token
    path("token/login/", CustomAuthToken.as_view(), name="login-token"),
    path("token/logout/", DiscardAuthToken.as_view(), name="logout-token"),
    # login jwt
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
