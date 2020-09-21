from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('mentoring/', include('mentoring.urls')),
    path('admin/', admin.site.urls),
]
