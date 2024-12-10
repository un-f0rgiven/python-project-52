from django.contrib import admin

from task_manager.statuses.models import Status


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
