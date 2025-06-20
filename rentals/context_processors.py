from .models import SiteSettings, SocialMedia, FAQ

def site_settings(request):
    """
    Add site_settings to the context of all templates, including the Django admin.
    """
    return {
        'site_settings': SiteSettings.get_settings()
    }

def social_media_links(request):
    """
    Add active social media links to the context of all templates.
    """
    return {
        'social_media_links': SocialMedia.objects.filter(is_active=True)
    }

def faqs(request):
    """
    Add active FAQs to the context of all templates.
    """
    return {
        'global_faqs': FAQ.objects.filter(is_active=True).order_by('order', 'id')[:5]
    } 