import csv

from django.contrib import admin, messages
from django.http import HttpResponse

from .forms import generate_unique_pseudonym
from .models import Faculty, Program, Mentor, Mentee


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'ask_for_phone', 'ask_for_program', 'deadline']
    ordering = ['slug']


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['faculty']
    ordering = ['slug']


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'qualification', 'supervision', 'created']
    list_filter = ['faculty', 'program']
    ordering = ['first_name', 'last_name']
    actions = ['export_as_csv', 'generate_nickname']

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

    def generate_nickname(self, request, queryset):
        counter = 0
        for mentor in queryset:
            if mentor.nick:
                continue
            mentor.nick = generate_unique_pseudonym(mentor)
            mentor.save()
            counter += 1

        self.message_user(request, f"Es wurden {counter} Mentor*innen aktualisiert.", messages.SUCCESS)
    generate_nickname.short_description = "Zufällig Nicknamen generieren"


@admin.register(Mentee)
class MenteeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'mentor', 'created']
    list_filter = ['mentor']
    ordering = ['first_name', 'last_name']
