from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:faculty_slug>/create/', views.MentorCreate.as_view(), name='create'),
    path('<slug:faculty_slug>/create/success/', views.SuccessView.as_view(), name='success'),
    path('token/<token>', views.TokenView.as_view(), name='token'),
    path('delete/', views.MentorDelete.as_view(), name='delete'),
]
