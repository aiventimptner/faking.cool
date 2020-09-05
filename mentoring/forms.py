import jwt

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


class MentorForm(forms.ModelForm):
    privacy = forms.BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        faculty = kwargs.pop('faculty', None)
        super().__init__(*args, **kwargs)
        self.fields['faculty'].initial = faculty
        self.fields['program'].queryset = Program.objects.order_by('name').filter(faculty=faculty)

        if faculty.ask_for_phone:
            self.fields['phone'].required = True

        if faculty.ask_for_program:
            self.fields['program'].required = True

        if not faculty.ask_for_phone:
            self.fields['phone'].widget.attrs['disabled'] = True

        if not faculty.ask_for_program:
            self.fields['program'].widget.attrs['disabled'] = True

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        return data.title()

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        return data.title()

    def clean_email(self):
        data = self.cleaned_data['email']
        return data.lower()

    def clean(self):
        cleaned_data = super().clean()
        faculty = cleaned_data.get('faculty')
        phone = cleaned_data.get('phone', None)
        program = cleaned_data.get('program')
        if faculty.ask_for_phone:
            if not phone:
                self.add_error('phone', "Es wird deine Mobilnummer benötigt.")

        if faculty.ask_for_program:
            if not program:
                self.add_error('program', "Es wird dein Studiengang benötigt.")

        if program.faculty != faculty:
            self.add_error('program', "Es können nur Studiengänge passend zur Fakultät ausgewählt werden.")

        if date.today() > faculty.deadline:
            raise forms.ValidationError("Die Anmeldefrist ist bereits vorbei!", code='registration closed')

    def send_email(self, request):
        faculty = self.cleaned_data['faculty']
        payload = {
            'iss': self.cleaned_data['email'],
            'iat': timezone.now(),
            'exp': datetime.combine(faculty.deadline, time()) - timedelta(weeks=1),  # TODO fix wrong time
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256').decode('utf8')
        data = {
            'name': self.cleaned_data['first_name'],
            'link': request.build_absolute_uri(reverse('mentoring:token', kwargs={'token': token})),
            'date': faculty.deadline - timedelta(weeks=1),
            'faculty': faculty
        }
        message = render_to_string('mentoring/mail/mentor.md', data)
        send_mail(  # TODO set 'reply to' to fara mail
            "Du hast dich erfolgreich registriert.",
            message,
            settings.EMAIL_HOST_USER,
            [self.cleaned_data['email']],
            html_message=markdown(message)
        )

    class Meta:
        model = Mentor
        fields = ['first_name', 'last_name', 'email', 'phone', 'faculty', 'program', 'qualification', 'supervision']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'email': forms.TextInput(attrs={'class': 'uk-input'}),
            'phone': forms.TextInput(attrs={'class': 'uk-input'}),
            'faculty': forms.HiddenInput(),
            'program': forms.Select(attrs={'class': 'uk-select'}),
            'qualification': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
            'supervision': forms.CheckboxInput(attrs={'class': 'uk-checkbox'}),
        }
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail Adresse",
            'phone': "Mobilnummer",
            'faculty': "Fakultät",
            'program': "Studiengang",
            'qualification': "Qualifizierung",
            'supervision': "Supervision",
        }
        error_messages = {
            'email': {
                'unique': "Ein Student oder eine Studentin mit dieser E-Mail Adresse ist bereits registriert.",
            }
        }


class MenteeForm(forms.ModelForm):
    MENTOR_LIST = [(mentor.pk, mentor.slug) for mentor in Mentor.objects.all()]

    mentor = forms.ChoiceField(
        choices=[('', "---------")] + MENTOR_LIST,
        widget=forms.Select(attrs={'class': 'uk-select'}),
        label='Mentor bzw. Mentorin',
        required=True,
    )
    privacy = forms.BooleanField(required=True)

    def clean_mentor(self):
        data = self.cleaned_data['mentor']
        try:
            mentor = Mentor.objects.get(pk=data)

        except ObjectDoesNotExist:
            raise ValidationError("Ein Mentor bzw. eine Mentorin mit dieser ID existiert nicht.")

        return mentor

    def send_email(self, request):
        first_name = self.cleaned_data['first_name']
        email = self.cleaned_data['email']
        mentor = self.cleaned_data['mentor']
        message = render_to_string('mentoring/mail/mentee.md', {'name': first_name, 'faculty': mentor.faculty})
        send_mail(  # TODO set 'reply to' to fara mail
            "Du hast dich erfolgreich registriert.",
            message,
            settings.EMAIL_HOST_USER,
            [email],
            html_message=markdown(message)
        )

    class Meta:
        model = Mentee
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'mentor']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'last_name': forms.TextInput(attrs={'class': 'uk-input'}),
            'email': forms.EmailInput(attrs={'class': 'uk-input'}),
            'phone': forms.TextInput(attrs={'class': 'uk-input'}),
            'address': forms.TextInput(attrs={'class': 'uk-input'}),
        }
        labels = {
            'first_name': "Vorname",
            'last_name': "Nachname",
            'email': "E-Mail Adresse",
            'phone': "Mobilnummer",
            'address': 'Anschrift',
        }
        error_messages = {
            'email': {
                'unique': "Ein Student oder eine Studentin mit dieser E-Mail Adresse ist bereits registriert.",
            }
        }
