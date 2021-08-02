import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Program, Mentor


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['faculty']


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created']
    list_filter = ['program__faculty']
    ordering = ['first_name', 'last_name']
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="mentoring.csv"'

        meta = self.model._meta
        field_names = [field.name for field in meta.get_fields()]

        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response
    export_as_csv.short_description = "Auswahl als CSV exportieren"
