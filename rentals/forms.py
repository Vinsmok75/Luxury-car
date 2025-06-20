from django import forms
from django.forms import inlineformset_factory
from .models import Car, CarImage, ContactMessage, Booking, SiteSettings, Customer, SocialMedia, FAQ

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4}),
        }

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        exclude = ['rating', 'total_reviews', 'created_at', 'updated_at', 'featured']

class CarImageForm(forms.ModelForm):
    class Meta:
        model = CarImage
        fields = ['image', 'is_primary', 'alt_text']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'alt_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

CarImageFormSet = inlineformset_factory(
    Car, CarImage,
    fields=['image', 'is_primary', 'alt_text'],
    extra=3,
    can_delete=True
)

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['site_name', 'site_logo']
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site_logo': forms.FileInput(attrs={'class': 'form-control'})
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['car', 'customer', 'start_date', 'end_date', 'status', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    class Meta:
        model = Customer
        fields = ['phone', 'address', 'driver_license']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.user.first_name = self.cleaned_data['first_name']
        customer.user.last_name = self.cleaned_data['last_name']
        customer.user.email = self.cleaned_data['email']
        
        if commit:
            customer.user.save()
            customer.save()
        
        return customer

class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['platform', 'url', 'is_active']
        widgets = {
            'url': forms.URLInput(attrs={'placeholder': 'https://...', 'class': 'form-control'}),
        }

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'is_active', 'order']
        widgets = {
            'question': forms.TextInput(attrs={'placeholder': 'Enter question here', 'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter answer here', 'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# ===== urls.py (main project) =====
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rentals.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)