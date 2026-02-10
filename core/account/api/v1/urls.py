from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenObtainPairView
)
from .views import *


app_name = "api-v1"
urlpatterns = [
 

   #login token
    path('token/login/', ObtainAuthToken.as_view(),name="login-token"),
    path('token/logout/', DiscardAuthToken.as_view(),name="logout-token"),

   #login jwt
    path('jwt/create/', TokenObtainPairView.as_view(),name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    

]
