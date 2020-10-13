from django.db import models
from django.core.validators import validate_email, RegexValidator

validate_color = RegexValidator(regex=r'^#[0-9A-F]{6}$',
                                message="Die Farben sind nur als Hexadezimal-Code erlaubt.")

validate_phone = RegexValidator(regex=r'^\+[1-9]{1}[0-9]{3,14}$',
                                message="Die Mobilnummer ist nur im Format '+49123456789' erlaubt.")


class Faculty(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=10, validators=[validate_color])
    ask_for_phone = models.BooleanField(default=False)
    ask_for_program = models.BooleanField(default=True)
    deadline = models.DateField()

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nick = models.SlugField(unique=True, null=True)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone = models.CharField(max_length=20, validators=[validate_phone], blank=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, blank=True, null=True)
    qualification = models.BooleanField(default=True)
    supervision = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Mentee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, validators=[validate_phone])
    address = models.CharField(max_length=255)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
