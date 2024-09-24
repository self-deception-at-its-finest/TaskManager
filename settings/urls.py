""" URL configuration for project """

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from application.views import registration

urlpatterns = [
    path('manager/', admin.site.urls),
    path('registration', registration),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
