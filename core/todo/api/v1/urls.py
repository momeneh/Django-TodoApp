from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "api-v1"
urlpatterns = [


]

router = DefaultRouter()
router.register('',views.TaskModelViewSet,basename = 'todo') 
urlpatterns += router.urls