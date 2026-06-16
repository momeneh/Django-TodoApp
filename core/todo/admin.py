from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    model = Task
    list_display = ("user", "title", "done")


admin.site.register(Task, TaskAdmin)
