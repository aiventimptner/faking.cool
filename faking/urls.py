from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('', lambda request: render(request, 'landing_page.html')),
    path('admin/', admin.site.urls),
]
