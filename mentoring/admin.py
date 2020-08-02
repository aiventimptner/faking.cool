import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Mentor, Faculty, Program


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'qualification', 'supervision', 'created')
    list_filter = ('faculty', 'program')
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


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    pass


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    pass
