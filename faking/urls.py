from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('mentoring:index')),
    path('mentoring/', include('mentoring.urls')),
    path('admin/', admin.site.urls),
]
