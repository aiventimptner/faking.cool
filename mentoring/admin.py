from django.contrib import admin

from .models import Mentor, Faculty, Program

admin.site.register(Mentor)
admin.site.register(Faculty)
admin.site.register(Program)

# TODO add filters for faculty
# TODO export as csv/excel
