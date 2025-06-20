from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Our custom admin URLs should come before Django's admin
    path('', include('rentals.urls')),
    # Django's built-in admin - change the URL to avoid conflicts
    path('django-admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)