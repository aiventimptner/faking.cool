import jwt

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .models import Faculty, Mentor
from .forms import MentorForm, MenteeForm


class IndexView(generic.ListView):
    template_name = 'mentoring/index.html'
    context_object_name = 'faculty_list'

    def get_queryset(self):
        return Faculty.objects.order_by('slug')


class MentorCreate(generic.edit.CreateView):
    template_name = 'mentoring/mentor/form.html'
    form_class = MentorForm
    success_url = 'success/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty_slug'])
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty_slug'])
        return kwargs
    
    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)


class SuccessView(generic.TemplateView):
    template_name = 'mentoring/mentor/success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['faculty'] = get_object_or_404(Faculty, slug=self.kwargs['faculty_slug'])
        return context


class TokenView(generic.TemplateView):
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


class MentorDelete(generic.edit.DeleteView):
    model = Mentor
    success_url = reverse_lazy('mentoring:delete')


class MenteeCreate(generic.edit.CreateView):
    template_name = 'mentoring/mentee/form.html'
    form_class = MenteeForm
    success_url = 'success/'

    def form_valid(self, form):
        form.send_email(self.request)
        return super().form_valid(form)


class MenteeSuccess(generic.TemplateView):
    template_name = 'mentoring/mentee/success.html'
