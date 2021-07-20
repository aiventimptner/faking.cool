from django import forms
from django.core.exceptions import ValidationError

from .models import Program, Mentor


class MentorForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True)

    class Meta:
        model = Mentor
        fields = ['first_name', 'last_name', 'email', 'phone', 'program']
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail-Adresse",
            'phone': "Mobilnummer",
            'program': "Studiengang",
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': "input"}),
            'last_name': forms.TextInput(attrs={'class': "input"}),
            'email': forms.EmailInput(attrs={'class': "input"}),
            'phone': forms.TextInput(attrs={'class': "input"}),
            'program': forms.Select(attrs={'class': "select"}),
        }

    def __init__(self, *args, **kwargs):
        self.faculty = kwargs.pop('faculty', None)
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.filter(faculty=self.faculty).order_by('name')

    def clean_first_name(self):
        data = self.cleaned_data['first_name'].title()
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name'].title()
        return data

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        if data.split('@')[1] not in ['st.ovgu.de', 'ovgu.de']:
            raise ValidationError("Es sind nur E-Mail-Adressen der "
                                  "Otto-von-Guericke-Universität Magdeburg erlaubt.", code='blocked')
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone'].replace(' ', '')

        # Define allowed values
        allowed_values = set([str(x) for x in range(10)])  # 0-9
        allowed_values.update(['+', '-', '/'])

        # Check for invalid values
        for value in data:
            if value not in allowed_values:
                raise ValidationError("Es können nur Zahlen (0-9) und einige "
                                      "Symbole (+, -, /) verwendet werden.", code='invalid')

        # Check for country code
        if data.startswith('00'):
            data = '+' + data[2:]

        if not data.startswith('+'):
            raise ValidationError("Bitte gibt deine Mobilnummer inklusive "
                                  "Ländervorwahl (z.B. +49, 0049) an.", code='ambiguous')

        # Remove unnecessary values
        data = '+' + data[1:].replace('+', '')
        data = data.replace('-', '').replace('/', '')

        return data
