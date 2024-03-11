
from django.urls import path
from . views import TaskListView,MyDayView

urlpatterns = [
    path('', view=TaskListView.as_view(), name='home'),
    path('myday/', view=MyDayView.as_view(), name='myday')
]