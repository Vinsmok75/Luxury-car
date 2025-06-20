from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Car, CarImage, ContactMessage, SiteSettings, SocialMedia, FAQ

# Customize admin site
admin.site.site_header = "Car Rental Administration"
admin.site.site_title = "Car Rental Admin Portal"
admin.site.index_title = "Welcome to Car Rental Admin Portal"

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'price_per_day', 'availability_status']
    list_filter = ['brand', 'transmission', 'fuel_type', 'availability_status']
    search_fields = ['name', 'brand', 'model']
    inlines = [CarImageInline]

class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name']

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'is_active']
    list_filter = ['platform', 'is_active']
    list_editable = ['is_active']

class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'order']
    list_filter = ['is_active']
    list_editable = ['is_active', 'order']
    search_fields = ['question', 'answer']

admin.site.register(Car, CarAdmin)
admin.site.register(CarImage)
admin.site.register(ContactMessage)
admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(FAQ, FAQAdmin)