from django.urls import path
from django.shortcuts import redirect

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('mentor/', lambda request: redirect('mentoring:index')),
    path('mentor/<slug:faculty>/', views.MentorCreate.as_view(), name='mentor-create'),
    path('mentor/<slug:faculty>/success/', views.MentorSuccess.as_view(), name='mentor-success'),
    path('token/<token>', views.MentorToken.as_view(), name='mentor-token'),
    path('mentor/delete/', views.MentorDelete.as_view(), name='mentor-delete'),
    path('mentee/', views.MenteeCreate.as_view(), name='mentee-create'),
    path('mentee/success/', views.MenteeSuccess.as_view(), name='mentee-success'),
]
