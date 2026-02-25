from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

app_name = "account"
urlpatterns = [
    path("api/v1/", include("account.api.v1.urls")),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
]
