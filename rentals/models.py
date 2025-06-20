from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
import os

class Car(models.Model):
    TRANSMISSION_CHOICES = [
        ('automatic', 'Automatic'),
        ('manual', 'Manual'),
    ]
    
    FUEL_CHOICES = [
        ('gasoline', 'Gasoline'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
    ]

    # Basic Information
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField(blank=True, help_text="Detailed description of the car")
    phone_number = models.CharField(max_length=20, blank=True, help_text="Contact phone number for this car")
    
    # Rental Information
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Technical Specifications
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    seats = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(9)])
    doors = models.PositiveIntegerField(validators=[MinValueValidator(2), MaxValueValidator(5)])
    engine_specs = models.CharField(max_length=50, help_text="e.g., 1.8L, 2.0L Turbo")
    air_conditioning = models.BooleanField(default=True)
    mileage = models.PositiveIntegerField(help_text="Total mileage in km")
    color = models.CharField(max_length=30)
    
    # Additional Features
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, 
                               validators=[MinValueValidator(0), MaxValueValidator(5)])
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Meta Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model}"
    
    def get_absolute_url(self):
        return reverse('car_detail', kwargs={'pk': self.pk})
    
    @property
    def is_available(self):
        return self.availability_status == 'available'

class CarImage(models.Model):
    car = models.ForeignKey(Car, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-is_primary', 'id']
    
    def __str__(self):
        return f"{self.car.name} - Image {self.id}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    driver_license = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Booking {self.id} - {self.car} ({self.status})"
    
    def get_duration(self):
        return (self.end_date - self.start_date).days

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Car Rental Site')
    site_logo = models.ImageField(upload_to='site/', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def save(self, *args, **kwargs):
        if SiteSettings.objects.exists() and not self.pk:
            # If a SiteSettings instance exists and we're trying to create a new one
            return
        return super(SiteSettings, self).save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        return cls.objects.first() or cls.objects.create()

    def __str__(self):
        return self.site_name

class SocialMedia(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('youtube', 'YouTube'),
        ('pinterest', 'Pinterest'),
        ('tiktok', 'TikTok'),
    ]
    
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Social Media Link'
        verbose_name_plural = 'Social Media Links'
    
    def __str__(self):
        return self.get_platform_display()

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which the FAQ appears")
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.question