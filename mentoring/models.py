from django.db import models


class Program(models.Model):
    FMB = 'MB'
    FEIT = 'EIT'
    FVST = 'VST'
    FMA = 'MA'
    FACULTIES = [
        (FMB, 'Maschinenbau'),
        (FEIT, 'Elektro- & Informationstechnik'),
        (FVST, 'Verfahrens- & Systemtechnik'),
        (FMA, 'Mathematik'),
    ]
    faculty = models.CharField(max_length=3, choices=FACULTIES)
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Mentor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
