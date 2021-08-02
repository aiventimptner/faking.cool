from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'faking/index.html')),
    path('mentoring/', include('mentoring.urls')),
    path('votes/', include('votes.urls')),
    path('admin/', admin.site.urls),
]
