from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('cars/', views.cars_list, name='cars_list'),
    path('cars/<int:pk>/', views.car_detail, name='car_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Admin authentication
    path('admin-login/', auth_views.LoginView.as_view(
        template_name='rentals/admin/login.html'
    ), name='admin_login'),
    path('admin-logout/', auth_views.LogoutView.as_view(), name='admin_logout'),
    
    # Admin dashboard
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Cars management
    path('dashboard/cars/', views.admin_cars_list, name='admin_cars_list'),
    path('dashboard/cars/add/', views.admin_add_car, name='admin_add_car'),
    path('dashboard/cars/<int:pk>/edit/', views.admin_edit_car, name='admin_edit_car'),
    path('dashboard/cars/<int:pk>/delete/', views.admin_delete_car, name='admin_delete_car'),
    
    # Bookings management
    path('dashboard/bookings/', views.admin_bookings_list, name='admin_bookings_list'),
    path('dashboard/bookings/<int:pk>/view/', views.admin_view_booking, name='admin_view_booking'),
    path('dashboard/bookings/<int:pk>/edit/', views.admin_edit_booking, name='admin_edit_booking'),
    
    # Customers management
    path('dashboard/customers/', views.admin_customers_list, name='admin_customers_list'),
    path('dashboard/customers/<int:pk>/view/', views.admin_view_customer, name='admin_view_customer'),
    path('dashboard/customers/<int:pk>/edit/', views.admin_edit_customer, name='admin_edit_customer'),
    
    # Messages management
    path('dashboard/messages/', views.admin_messages_list, name='admin_messages_list'),
    path('dashboard/messages/<int:pk>/mark-read/', views.admin_mark_message_read, name='admin_mark_message_read'),
    
    # Social Media management
    path('dashboard/social-media/', views.admin_social_media_list, name='admin_social_media_list'),
    path('dashboard/social-media/add/', views.admin_add_social_media, name='admin_add_social_media'),
    path('dashboard/social-media/<int:pk>/edit/', views.admin_edit_social_media, name='admin_edit_social_media'),
    path('dashboard/social-media/<int:pk>/delete/', views.admin_delete_social_media, name='admin_delete_social_media'),
    
    # FAQ management
    path('dashboard/faq/', views.admin_faqs_list, name='admin_faqs_list'),
    path('dashboard/faq/add/', views.admin_add_faq, name='admin_add_faq'),
    path('dashboard/faq/<int:pk>/edit/', views.admin_edit_faq, name='admin_edit_faq'),
    path('dashboard/faq/<int:pk>/delete/', views.admin_delete_faq, name='admin_delete_faq'),
    
    # Site settings
    path('dashboard/settings/', views.admin_site_settings, name='admin_site_settings'),
]