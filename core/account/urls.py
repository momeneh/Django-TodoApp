from django.urls import path,include
from . import views
from django.contrib.auth.views import LoginView,LogoutView
app_name = "account"
urlpatterns = [
   
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(next_page="/"),name="logout"),

]

