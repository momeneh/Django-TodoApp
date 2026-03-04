from . import views
from rest_framework.routers import DefaultRouter
import pprint

app_name = "api-v1"
urlpatterns = []

router = DefaultRouter()
router.register("", views.TaskModelViewSet, basename="todo")
urlpatterns += router.urls
# print(router.get_urls())
