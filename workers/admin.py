from django.contrib import admin
from .models import Worker
from django.contrib.admin import ModelAdmin


@admin.register(Worker)
class WorkerAdmin(ModelAdmin):
    exclude = ('employment_date', 'position',)
    list_display = (Worker.get_fullname, 'position', 'employment_date', 'salary', 'chief',)
    search_fields = ('first_name', 'last_name', 'patronymic', 'position',)
    list_filter = ('position',)
    list_editable = ('salary',)

