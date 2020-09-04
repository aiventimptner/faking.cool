from django.db import models
from django.core.validators import validate_email, RegexValidator

# Custom validators

validate_color = RegexValidator(regex=r'[0-9A-F]{6}',
                                message="Es sind nur Farben als Hexadezimal-Code erlaubt.")
validate_ovgu_email = RegexValidator(regex=r'(\w+\.)?\w+@st.ovgu.de',
                                     message="Es sind nur Adressen mit der Domain 'st.ovgu.de' erlaubt.")
validate_phone = RegexValidator(regex=r'01\d{2}\/\d{6,7}',
                                message="Die Mobilnummer ist nur im Format '0123/456789' erlaubt.")
validate_address = RegexValidator(regex=r'.*\,\s\d{5}\s\w{3,}',
                                  message="Die Anschrift muss im Format 'Straße Nr., PLZ Stadt' "
                                          "angegeben werden.")


# Models

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=6, validators=[validate_color])
    ask_for_phone = models.BooleanField(default=False)
    ask_for_program = models.BooleanField(default=True)
    deadline = models.DateField()

    def __str__(self):
        return self.name

    def color_as_hex(self):
        return '#' + str(self.color)


class Program(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Mentor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_ovgu_email])
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

    def slug(self):
        first = str(self.first_name)[0] + str(self.first_name)[-1]
        last = str(self.last_name)[0] + str(self.last_name)[-1]
        check = sum([ord(letter) - 64 for letter in list(str(self.full_name()).replace(' ', '').upper())])
        return f"{first.upper()}{last.upper()}{check}"


class Mentee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, validators=[validate_email])
    phone = models.CharField(max_length=20, validators=[validate_phone])
    address = models.CharField(max_length=255, validators=[validate_address])
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
