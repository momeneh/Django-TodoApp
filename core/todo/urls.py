from django.urls import path,include
from . import views
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


app_name = "todo"
urlpatterns = [
   
    path('',views.TaskListView.as_view(),name="task-list"),
    path('create/',views.TaskCreateView.as_view(),name="task-create"),
    path('<int:pk>/edit',views.TaskUpdateView.as_view(),name="task-edit"),
    path('<int:pk>/done',views.TaskDone.as_view(),name="task-done"),
    path('<int:pk>/delete',views.TaskDeleteView.as_view(),name="task-delete"),

]

