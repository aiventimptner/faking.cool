from datetime import timedelta
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import reverse
from django.utils import timezone

from .models import Decision, Option, Vote, Invitation, Team


class DecisionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['voters'].required = True
        self.fields['voters'].queryset = User.objects.filter(
            teams__in=self.user.teams.all(),
        ).distinct().order_by('first_name', 'last_name')
        self.fields['voters'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return obj.get_full_name()

    def clean_start(self):
        data = self.cleaned_data['start']
        if timezone.now() - timedelta(minutes=5) > data:
            raise ValidationError("Der Zeitpunkt darf höchstens 5 Minuten in der Vergangenheit liegen.",
                                  code='invalid')

        return data

    def clean_end(self):
        data = self.cleaned_data['end']
        if timezone.now() + timedelta(minutes=5) > data:
            raise ValidationError("Der Zeitpunkt muss wenigstens 5 Minuten in der Zukunft liegen.",
                                  code='invalid')

        return data

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        diff = 15  # Minutes

        if start and end:
            if start + timedelta(minutes=diff) > end:
                raise ValidationError(
                    f"Die Dauer von Abstimmungen muss mind. {diff} Minuten betragen.",
                    code='invalid',
                )

    class Meta:
        model = Decision
        fields = ['subject', 'voters', 'start', 'end']
        labels = {
            'subject': "Gegenstand",
            'voters': "Stimmberechtigt",
            'start': "Beginn",
            'end': "Ende",
        }
        widgets = {
            'subject': forms.Textarea(attrs={
                'class': "textarea has-fixed-size",
                'placeholder': "Es sind maximal 255 Zeichen erlaubt.",
                'rows': 2,
            }),
            'voters': forms.SelectMultiple(attrs={
                'size': 6,
            }),
            'start': forms.DateTimeInput(attrs={
                'class': "input",
                'placeholder': "31.12.2099 16:30",
            }),
            'end': forms.DateTimeInput(attrs={
                'class': "input",
                'placeholder': "31.12.2099 16:45",
            }),
        }


class VoteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.decision = kwargs.pop('decision')
        super().__init__(*args, **kwargs)
        self.fields['option'].queryset = Option.objects.filter(decision=self.decision)

    class Meta:
        model = Vote
        fields = ['option']
        widgets = {
            'option': forms.RadioSelect(attrs={
                'class': "radio",
            }),
        }


class InvitationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if self.user.is_superuser:
            self.fields['teams'].queryset = Team.objects.all()
        else:
            self.fields['teams'].queryset = Team.objects.filter(members__in=[self.user])

    def clean_expiry(self):
        data = self.cleaned_data['expiry']
        diff = data - timezone.now()
        value = round(diff.total_seconds() / 3600)
        if value not in [8, 24, 168]:
            raise ValidationError("Es können nur die vorgegebenen Fristen verwendet werden.", code='invalid')

        return data

    class Meta:
        model = Invitation
        fields = ['teams', 'expiry']
        labels = {
            'teams': "Organ(e)",
            'expiry': "Gültigkeit",
        }
        widgets = {
            'teams': forms.CheckboxSelectMultiple(),
            'expiry': forms.HiddenInput(),
        }


class JoinTeamForm(forms.Form):
    token = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': "input",
            'autofocus': "",
        }),
        required=True,
    )

    def clean_token(self):
        data = self.cleaned_data['token']

        try:
            invitation = Invitation.objects.get(token=data)
        except ObjectDoesNotExist:
            raise ValidationError("Der Token ist ungültig.", code='invalid')

        if timezone.now() > invitation.expiry:
            raise ValidationError("Der Token ist abgelaufen.", code='invalid')

        return data


class RegistrationForm(forms.ModelForm):
    token = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

    def clean_token(self):
        data = self.cleaned_data['token']

        if not data:
            raise ValidationError("Die Registrierung ist nur mit einer Einladung möglich!", code='unauthorized')

        try:
            invitation = Invitation.objects.get(token=data)
        except ObjectDoesNotExist:
            raise ValidationError("Die verwendete Einladung ist ungültig.", code='invalid')

        if timezone.now() > invitation.expiry:
            raise ValidationError("Der verwendete Einladung ist abgelaufen.", code='expired')

        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        return data.title()

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        return data.title()

    def clean_username(self):
        data = self.cleaned_data['username']
        return data.lower()

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[-1]

        if domain != 'st.ovgu.de':
            raise ValidationError("Es sind nur E-Mail-Adressen mit der angegebenen Domain erlaubt.", code='invalid')

        return data

    def send_email(self, request, secret):
        link = f"{request.scheme}://{request.get_host()}{reverse('password_change')}"
        send_mail(
            "Neuer Account erstellt",
            f"Hallo {self.cleaned_data['first_name']},\n\ndu kannst dich nun mit dem Benutzer "
            f"'{self.cleaned_data['username']}' und dem temporären Passwort '{secret}' "
            f"anmelden. Dein Passwort kannst du nach dem Login unter {link} ändern.\n\nViele Grüße\nFakIng",
            None,
            [self.cleaned_data['email']],
        )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input',
            }),
            'username': forms.TextInput(attrs={
                'class': 'input',
            }),
            'email': forms.TextInput(attrs={
                'class': 'input',
            }),
        }
