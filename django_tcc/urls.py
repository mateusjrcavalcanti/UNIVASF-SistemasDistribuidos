from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from django_tcc.core import views as core_views

urlpatterns = [
    path("", core_views.index),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
