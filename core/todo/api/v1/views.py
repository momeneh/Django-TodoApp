from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from .permissions import IsOwner
from .serializers import TaskSerializer
from ...models import Task


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TaskSerializer
    model = Task
    ordering_fields = ["-id"]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user.id)
