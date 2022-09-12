from django.contrib import admin

from .models import Project, WorkSession


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkSession)
class WorkSessionAdmin(admin.ModelAdmin):
    pass
