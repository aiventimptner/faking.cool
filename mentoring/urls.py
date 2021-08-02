from django.urls import path

from . import views

app_name = 'mentoring'
urlpatterns = [
    path('', views.MentorCreate.as_view(), name='mentor-create'),
    path('success/', views.MentorSuccess.as_view(), name='mentor-success'),
]
