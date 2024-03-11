from django.contrib import admin
from .models import Task, TaskTag, Tag, List

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'status', 'is_important', 'due_date', 'list', 'get_tags' )
    search_fields = ('title', 'status')
    search_help_text = 'Search tasks by title or status'
    list_filter = ('status', 'is_important')

    def get_tags(self, obj):
        return ", ".join([tag.title for tag in obj.tag.all()])

    get_tags.short_description = 'Tags'

class ListAdmin(admin.ModelAdmin):
    list_display = ('id', "title", "user")

    # def get_username(self, obj):
    #     return obj.user.username

    # get_username.short_description = 'Username'

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class TaskTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tagname', 'get_taskname')

    def get_tagname(self, obj):
        return obj.tag.title
    
    def get_taskname(self, obj):
        return obj.task.title

    get_tagname.short_description = 'Tagname'
    get_taskname.short_description = 'Taskname'

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskTag, TaskTagAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(List, ListAdmin)