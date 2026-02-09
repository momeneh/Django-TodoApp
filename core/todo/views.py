from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import Task
from django.urls import reverse_lazy,reverse
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

class TaskListView(LoginRequiredMixin,ListView):
  model = Task
  template_name = 'todo/list.html'
  context_object_name = 'tasks'
  ordering = 'id'

  def get_queryset(self):
    return self.model.objects.filter(user=self.request.user)

    
class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title']
    success_url = reverse_lazy("todo:task-list")

    def form_valid(self, form):
       form.instance.user = self.request.user
       return super().form_valid(form)
    
    def get(self,request,*args,**kwarg):
       return redirect(reverse("todo:task-list"))
    
class TaskUpdateView(LoginRequiredMixin,UpdateView):
    model = Task
    success_url = reverse_lazy("todo:task-list")
    fields = ['title']
    template_name = "todo/list.html"

    def get_queryset(self):
      return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
      context =  super().get_context_data(**kwargs)
      context['custom_action'] = reverse("todo:task-edit",kwargs={'pk':self.get_object().pk})
      return context

class TaskDeleteView(LoginRequiredMixin,DeleteView):
  model = Task
  success_url = reverse_lazy("todo:task-list")
  
  def get_queryset(self):
      return self.model.objects.filter(user=self.request.user)

  
class TaskDone(LoginRequiredMixin,View):
  def get(self,request,*args,**kwargs):
    queryset = Task.objects.filter(user=self.request.user)
    object = get_object_or_404(queryset, pk=kwargs.get('pk'))
    object.done = not(object.done)
    object.save()
    return redirect(reverse("todo:task-list"))