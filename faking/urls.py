from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'faking/landing_page.html'), name='landing_page'),
    path('mentoring/', include('mentoring.urls')),
    path('votes/', include('votes.urls')),
    path('admin/', admin.site.urls),
]
