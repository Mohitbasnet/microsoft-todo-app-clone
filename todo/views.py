from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views import View
from todo.models import Task, List
from datetime import datetime
from django.utils import timezone
from django.db.models import Q

# List all tasks
class TaskListView(ListView, LoginRequiredMixin):
    model = Task
    template_name = 'todo/home.html'
    context_object_name = 'task_list'
    paginate_by = 10

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the original context
        context = super().get_context_data(**kwargs)

        # Add your custom context data
        user = self.request.user
        lists = List.objects.filter(user=user)
        context['lists'] = lists

        return context
    
class MyDayView(ListView):
    model = Task
    template_name = 'todo/my_day.html'
    context_object_name = 'task_list'
    paginate_by = 10

    now = timezone.now()
    def get_queryset(self):
        user = self.request.user
        now = timezone.now().date()
        query = Q(user=user, due_date=now)
        return Task.objects.filter(query)
    
# class ListDetailView(View):
#     def get(self, request, *args, **kwargs):
#         tasks = 