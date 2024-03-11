from django.db import models
from .choices import StatusChoice
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel
from datetime import datetime, timedelta
from django.utils import timezone
import shortuuid
from django.utils.text import slugify

User = get_user_model()

def default_due_date():
    return timezone.now() + timedelta(days=1)

# One User can create multiple lists
class List(TimeStampedModel):
    title = models.CharField(max_length=15)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lists")
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title}-user-{self.user_id}"
    
    def save(self, *args, **kwargs):
        # Modify the slug field before saving
        self.slug = f"{slugify(self.title)}-{shortuuid.uuid()}"
        return super().save(*args, **kwargs)

# Tags
class Tag(TimeStampedModel):
    title = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.title

# Tasks
class Task(TimeStampedModel):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    status = models.CharField(choices=StatusChoice.CHOICE_LIST, max_length=20, default=StatusChoice.PENDING)
    is_important = models.BooleanField(default=False)
    due_date = models.DateField(default=default_due_date)
    due_time = models.TimeField(default=timezone.now)

    # Relationships
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    tag = models.ManyToManyField(Tag, related_name='tasks', through='TaskTag')

    def is_due_date_today(self, *args, **kwargs):
        return self.due_date == datetime.now().date() and self.status != StatusChoice.COMPLETED
    
    def is_task_missed(self, *args, **kwargs):
        return self.status != StatusChoice.COMPLETED and self.due_date <= datetime.now().date() and self.due_time < datetime.now().time()

    def save(self, *args, **kwargs):
        if not self.description:
            self.description = f"This task needs to be completed before {self.due_date.day}!"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

# TaskTag to maintain many to many relationships between Task and Tag 
class TaskTag(TimeStampedModel):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = ['tag_id', 'task_id'],
                name='unique_task_tag'
            )
        ]

    def __str__(self) -> str:
        return str(self.tag_id) + "-" + str(self.task_id)