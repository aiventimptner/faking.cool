import jwt

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, DeleteView

from .models import Faculty, Mentor
from .forms import MentorForm, MenteeForm


class IndexView(TemplateView):
    template_name = 'mentoring/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['faculties'] = Faculty.objects.all()
        return context


class MentorCreate(CreateView):
    template_name = 'mentoring/mentor/form.html'
    form_class = MentorForm
    success_url = 'success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty'])
        return kwargs
    
    def form_valid(self, form):
        form.send_email(self.request)
        print(self.request)
        # form.instance.faculty
        return super().form_valid(form)


class MentorSuccess(TemplateView):
    template_name = 'mentoring/mentor/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty'])
        return context


class MentorToken(TemplateView):
    template_name = 'mentoring/mentor/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        try:
            payload = jwt.decode(self.kwargs['token'], settings.SECRET_KEY)
            mentor = get_object_or_404(Mentor, email=payload['iss'])
            mentor.delete()

        except jwt.DecodeError:
            context['token'] = {
                'status': 'danger',
                'message': "Der Token ist ungültig.",
            }

        except jwt.ExpiredSignature:
            context['token'] = {
                'status': 'danger',
                'message': "Der Token ist abgelaufen. Bitte wende dich per E-Mail an deinen Fachschaftsrat.",
            }

        return context


class MentorDelete(DeleteView):
    model = Mentor
    success_url = reverse_lazy('mentoring:delete')


class MenteeCreate(CreateView):
    template_name = 'mentoring/mentee/form.html'
    form_class = MenteeForm
    success_url = 'success/'

    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)


class MenteeSuccess(TemplateView):
    template_name = 'mentoring/mentee/success.html'
