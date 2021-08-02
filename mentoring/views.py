from django.core.mail import send_mail
from django.views import generic

from .forms import MentorForm


class MentorCreate(generic.CreateView):
    template_name = 'mentoring/mentor_form.html'
    form_class = MentorForm
    success_url = 'success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['privacy'] = ("Wir verwenden deine Daten um mit dir Kontakt aufzunehmen. Dein vollständiger Name und "
                              "deine E-Mail-Adresse werden außerdem zur Anmeldung für die Mentoring-Schulung benötigt. "
                              "Nach Ablauf von 12 Monaten werden sämtliche Daten von uns gelöscht.")
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['faculty'] = self.request.GET.get('faculty')
        return kwargs
    
    def form_valid(self, form):
        send_mail(
            "Bestätigung deiner Registrierung",
            """Hallo %(first_name)s,

hiermit bestätigen wir deine Registrierung als Mentor:in. 
Wir werden dich erneut kontaktieren sobald es die ersten 
Informationen zur Mentoring-Schulung gibt.

Viele Grüße
Dein Fachschaftsrat""" % form.cleaned_data,
            None,
            [form.cleaned_data['email']]
        )
        return super().form_valid(form)


class MentorSuccess(generic.TemplateView):
    template_name = 'mentoring/success.html'
