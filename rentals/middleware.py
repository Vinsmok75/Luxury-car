from django.contrib import admin
from .models import SiteSettings

class DynamicAdminSiteMiddleware:
    """
    Middleware to dynamically set the admin site title, header, and index title
    based on the SiteSettings model.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Update admin site titles before processing the request
        if request.path.startswith('/admin/'):
            settings = SiteSettings.get_settings()
            site_name = settings.site_name
            
            admin.site.site_header = f"{site_name} Administration"
            admin.site.site_title = f"{site_name} Admin Portal"
            admin.site.index_title = f"Welcome to {site_name} Admin Portal"
        
        response = self.get_response(request)
        return response 