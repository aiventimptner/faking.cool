import jwt
import random

from datetime import datetime, date, time, timedelta
from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from markdown import markdown

from .models import Program, Mentor, Mentee


def generate_unique_pseudonym(mentor: Mentor):
    queryset = [mentor.nick for mentor in Mentor.objects.all()]
    first = mentor.first_name.upper()
    last = mentor.last_name.upper()
    value = ''.join(random.choices(first, k=3)) + ''.join(random.choices(last, k=3))

    while value in queryset:
        value = ''.join(random.choices(first, k=3)) + ''.join(random.choices(last, k=3))

    return value


class MentorModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nick


class MentorForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True)

    class Meta:
        model = Mentor
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'program',
            'qualification',
            'supervision',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'email': forms.EmailInput(attrs={'class': 'uk-input'}),
            'phone': forms.TextInput(attrs={'class': 'uk-input'}),
            'program': forms.Select(attrs={'class': 'uk-select'}),
            'qualification': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
            'supervision': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
        }
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail Adresse",
            'phone': "Mobilnummer",
            'program': "Studiengang",
            'qualification': "Qualifizierung",
            'supervision': "Supervision",
        }
        error_messages = {
            'email': {
                'unique': "Ein*e Student*in mit dieser E-Mail Adresse ist bereits registriert.",
            }
        }

    def __init__(self, *args, **kwargs):
        self.faculty = kwargs.pop('faculty', None)
        super().__init__(*args, **kwargs)
        self.fields['program'].queryset = Program.objects.order_by('name').filter(faculty=self.faculty)

        if self.faculty.ask_for_phone:
            self.fields['phone'].required = True

        else:
            self.fields['phone'].widget.attrs['disabled'] = True

        if self.faculty.ask_for_program:
            self.fields['program'].required = True

        else:
            self.fields['program'].widget.attrs['disabled'] = True

    def clean_first_name(self):
        data = self.cleaned_data['first_name'].title()
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name'].title()
        return data

    def clean_email(self):
        data = self.cleaned_data['email'].lower()
        if data.split('@')[1] != 'st.ovgu.de':
            raise ValidationError("Es sind nur E-Mail Adressen mit der Domain 'st.ovgu.de' erlaubt.", code='invalid')

        return data

    def clean(self):
        super().clean()

        if date.today() > self.faculty.deadline:
            raise ValidationError("Die Anmeldefrist ist bereits vorbei!", code='closed')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.faculty = self.faculty
        instance.nick = generate_unique_pseudonym(instance)

        if commit:
            instance.save()

        return instance

    def send_email(self, request):
        payload = {
            'iss': self.cleaned_data['email'],
            'iat': timezone.now(),
            'exp': datetime.combine(self.faculty.deadline, time()) - timedelta(weeks=1),  # TODO fix wrong time
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf8')
        data = {
            'name': self.cleaned_data['first_name'],
            'link': request.build_absolute_uri(reverse('mentoring:mentor-token', kwargs={'token': token})),
            'date': self.faculty.deadline - timedelta(weeks=1),
            'faculty': self.faculty
        }
        message = render_to_string('mentoring/mail/mentor.md', data)
        send_mail(  # TODO set 'reply to' to fara mail
            "Du hast dich erfolgreich registriert.",
            message,
            settings.EMAIL_HOST_USER,
            [self.cleaned_data['email']],
            html_message=markdown(message)
        )


class MenteeForm(forms.ModelForm):
    mentor = MentorModelChoiceField(
        queryset=Mentor.objects.all(),
        widget=forms.Select(attrs={'class': "uk-select"}),
        label="Mentor*in",
        required=True,
    )
    privacy = forms.BooleanField(required=True)

    class Meta:
        model = Mentee
        fields = ['first_name', 'last_name', 'phone', 'address', 'mentor']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'phone': forms.TextInput(attrs={'class': 'uk-input'}),
            'address': forms.TextInput(attrs={'class': 'uk-input'}),
        }
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'phone': "Mobilnummer",
            'address': "Anschrift",
        }
