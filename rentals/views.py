from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Car, ContactMessage, Booking, Customer, CarImage, SiteSettings, User, SocialMedia, FAQ
from .forms import ContactForm, CarForm, CarImageFormSet, SiteSettingsForm, BookingForm, CustomerForm, SocialMediaForm, FAQForm
from django.urls import reverse
from datetime import datetime

def home(request):
    # Instead of filtering by featured=True, just show the most recent available cars
    best_rated_cars = Car.objects.filter(availability_status='available').order_by('-rating')[:3]
    
    context = {
        'best_rated_cars': best_rated_cars,
    }
    return render(request, 'rentals/home.html', context)

def cars_list(request):
    # Get all cars and order by newest first
    cars = Car.objects.all().order_by('-created_at')
    
    # Debug logging
    print(f"Total cars in database: {cars.count()}")
    for car in cars[:5]:
        print(f"- {car.name} ({car.availability_status})")
    
    # Filtering
    brand_filter = request.GET.get('brand')
    fuel_filter = request.GET.get('fuel_type')
    transmission_filter = request.GET.get('transmission')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    search = request.GET.get('search')
    
    if brand_filter:
        cars = cars.filter(brand__icontains=brand_filter)
    if fuel_filter:
        cars = cars.filter(fuel_type=fuel_filter)
    if transmission_filter:
        cars = cars.filter(transmission=transmission_filter)
    if price_min:
        cars = cars.filter(price_per_day__gte=price_min)
    if price_max:
        cars = cars.filter(price_per_day__lte=price_max)
    if search:
        cars = cars.filter(
            Q(name__icontains=search) | 
            Q(brand__icontains=search) | 
            Q(model__icontains=search)
        )
    
    # Debug logging after filters
    print(f"Cars after filtering: {cars.count()}")
    
    # Pagination
    paginator = Paginator(cars, 12)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)
    
    # Get filter options
    brands = Car.objects.values_list('brand', flat=True).distinct()
    fuel_types = Car.FUEL_CHOICES
    transmission_types = Car.TRANSMISSION_CHOICES
    
    context = {
        'cars': cars_page,
        'brands': brands,
        'fuel_types': fuel_types,
        'transmission_types': transmission_types,
        'current_filters': {
            'brand': brand_filter,
            'fuel_type': fuel_filter,
            'transmission': transmission_filter,
            'price_min': price_min,
            'price_max': price_max,
            'search': search,
        }
    }
    return render(request, 'rentals/cars_list.html', context)

def car_detail(request, pk):
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        # Handle booking form submission
        pickup_date = request.POST.get('pickup_date')
        return_date = request.POST.get('return_date')
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email', '')  # Optional field
        phone_number = request.POST.get('phone_number')
        
        # Calculate total price based on the number of days
        start_date = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(return_date, '%Y-%m-%d').date()
        days = (end_date - start_date).days + 1  # Include the pickup day
        total_price = car.price_per_day * days
        
        # Create a temporary customer for non-logged in users
        user_defaults = {'first_name': customer_name}
        if customer_email:
            user_defaults['email'] = customer_email
            
        customer, created = Customer.objects.get_or_create(
            user=User.objects.get_or_create(
                username=f"guest_{phone_number}",
                defaults=user_defaults
            )[0],
            defaults={
                'phone': phone_number,
                'address': 'Provided at pickup',
                'driver_license': 'Verified at pickup'
            }
        )
        
        # Create the booking
        notes = f"Booking made by {customer_name} with phone {phone_number}"
        if customer_email:
            notes += f" and email {customer_email}"
            
        booking = Booking.objects.create(
            car=car,
            customer=customer,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            status='pending',
            notes=notes
        )
        
        messages.success(request, f'Thank you, {customer_name}! Your booking request for {car.name} has been received. We will contact you shortly.')
        return redirect('car_detail', pk=car.pk)
    
    related_cars = Car.objects.filter(
        brand=car.brand, 
        availability_status='available'
    ).exclude(pk=car.pk)[:3]
    
    context = {
        'car': car,
        'related_cars': related_cars,
    }
    return render(request, 'rentals/car_detail.html', context)

def about(request):
    return render(request, 'rentals/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    faqs = FAQ.objects.filter(is_active=True).order_by('order', 'id')
    
    context = {
        'form': form,
        'faqs': faqs
    }
    return render(request, 'rentals/contact.html', context)

# Admin Dashboard Views
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    total_cars = Car.objects.count()
    available_cars = Car.objects.filter(availability_status='available').count()
    rented_cars = Car.objects.filter(availability_status='rented').count()
    messages_count = ContactMessage.objects.filter(is_read=False).count()
    total_bookings = Booking.objects.count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    total_customers = Customer.objects.count()
    
    recent_cars = Car.objects.all()[:5]
    recent_bookings = Booking.objects.all()[:5]
    recent_messages = ContactMessage.objects.all()[:5]
    
    context = {
        'total_cars': total_cars,
        'available_cars': available_cars,
        'rented_cars': rented_cars,
        'messages_count': messages_count,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'total_customers': total_customers,
        'recent_cars': recent_cars,
        'recent_bookings': recent_bookings,
        'recent_messages': recent_messages,
    }
    return render(request, 'rentals/admin/dashboard.html', context)

@login_required
def admin_cars_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    cars = Car.objects.all().order_by('-created_at')  # Sort by newest first
    paginator = Paginator(cars, 20)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)
    
    context = {'cars': cars_page}
    return render(request, 'rentals/admin/cars_list.html', context)

@login_required
def admin_add_car(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        formset = CarImageFormSet(request.POST, request.FILES)
        
        # Debug logging
        print("Form data:", request.POST)
        print("Files:", request.FILES)
        
        if form.is_valid() and formset.is_valid():
            car = form.save()
            formset.instance = car
            formset.save()
            messages.success(request, f'Car "{car.name}" has been added successfully!')
            return redirect('admin_cars_list')
        else:
            # Add error messages for debugging
            if not form.is_valid():
                print("Form errors:", form.errors)
                messages.error(request, f'Form errors: {form.errors}')
            if not formset.is_valid():
                print("Formset errors:", formset.errors)
                messages.error(request, f'Image formset errors: {formset.errors}')
    else:
        form = CarForm()
        formset = CarImageFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Add New Car'
    }
    return render(request, 'rentals/admin/car_form.html', context)

@login_required
def admin_edit_car(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    car = get_object_or_404(Car, pk=pk)
    
    if request.method == 'POST':
        form = CarForm(request.POST, instance=car)
        formset = CarImageFormSet(request.POST, request.FILES, instance=car)
        
        if form.is_valid() and formset.is_valid():
            car = form.save()
            formset.save()
            messages.success(request, f'Car "{car.name}" has been updated successfully!')
            return redirect('admin_cars_list')
    else:
        form = CarForm(instance=car)
        formset = CarImageFormSet(instance=car)
    
    context = {
        'form': form,
        'formset': formset,
        'car': car,
        'title': f'Edit Car: {car.name}'
    }
    return render(request, 'rentals/admin/car_form.html', context)

@login_required
def admin_delete_car(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    car = get_object_or_404(Car, pk=pk)
    if request.method == 'POST':
        car_name = car.name
        car.delete()
        messages.success(request, f'Car "{car_name}" has been deleted successfully!')
        return redirect('admin_cars_list')
    
    context = {'car': car}
    return render(request, 'rentals/admin/car_confirm_delete.html', context)

@login_required
def admin_bookings_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    bookings = Booking.objects.all().select_related('car', 'customer')
    
    # Filtering
    status_filter = request.GET.get('status')
    search = request.GET.get('search')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if search:
        bookings = bookings.filter(
            Q(car__name__icontains=search) |
            Q(customer__user__first_name__icontains=search) |
            Q(customer__user__last_name__icontains=search) |
            Q(customer__user__email__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(bookings, 20)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)
    
    context = {
        'bookings': bookings_page,
        'status_choices': Booking.STATUS_CHOICES,
        'current_filters': {
            'status': status_filter,
            'search': search,
        }
    }
    return render(request, 'rentals/admin/bookings_list.html', context)

@login_required
def admin_customers_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    customers = Customer.objects.all().select_related('user')
    
    # Search
    search = request.GET.get('search')
    if search:
        customers = customers.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(user__email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    customers_page = paginator.get_page(page_number)
    
    context = {
        'customers': customers_page,
        'search': search,
    }
    return render(request, 'rentals/admin/customers_list.html', context)

@login_required
def admin_messages_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    messages_list = ContactMessage.objects.all()
    
    # Filter by read/unread
    is_read = request.GET.get('is_read')
    search = request.GET.get('search')
    
    if is_read is not None:
        messages_list = messages_list.filter(is_read=(is_read == 'true'))
    if search:
        messages_list = messages_list.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(subject__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    messages_page = paginator.get_page(page_number)
    
    context = {
        'messages': messages_page,
        'current_filters': {
            'is_read': is_read,
            'search': search,
        }
    }
    return render(request, 'rentals/admin/messages_list.html', context)

@login_required
def admin_mark_message_read(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    message = get_object_or_404(ContactMessage, pk=pk)
    message.is_read = True
    message.save()
    
    messages.success(request, f"Message from {message.name} marked as read.")
    
    # Get the referring URL or default to the messages list
    redirect_url = request.META.get('HTTP_REFERER', reverse('admin_messages_list'))
    return redirect(redirect_url)

@login_required
def admin_site_settings(request):
    settings = SiteSettings.get_settings()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('admin_site_settings')
    else:
        form = SiteSettingsForm(instance=settings)
    
    return render(request, 'rentals/admin/site_settings.html', {
        'form': form,
        'settings': settings,
        'section': 'settings'
    })

@login_required
def admin_view_booking(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    # Calculate booking duration in days
    duration = (booking.end_date - booking.start_date).days
    
    context = {
        'booking': booking,
        'duration': duration,
    }
    return render(request, 'rentals/admin/booking_detail.html', context)

@login_required
def admin_edit_booking(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    booking = get_object_or_404(Booking, pk=pk)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Recalculate total price based on the number of days and car price
            days = (booking.end_date - booking.start_date).days + 1  # Include the pickup day
            booking.total_price = booking.car.price_per_day * days
            
            booking.save()
            messages.success(request, f'Booking #{booking.id} has been updated successfully!')
            return redirect('admin_bookings_list')
    else:
        form = BookingForm(instance=booking)
    
    context = {
        'form': form,
        'booking': booking,
    }
    return render(request, 'rentals/admin/booking_form.html', context)

@login_required
def admin_view_customer(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    customer = get_object_or_404(Customer, pk=pk)
    
    # Get customer's bookings
    bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
    
    context = {
        'customer': customer,
        'bookings': bookings,
    }
    return render(request, 'rentals/admin/customer_detail.html', context)

@login_required
def admin_edit_customer(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer.user.get_full_name()} has been updated successfully!')
            return redirect('admin_customers_list')
    else:
        form = CustomerForm(instance=customer)
    
    context = {
        'form': form,
        'customer': customer,
    }
    return render(request, 'rentals/admin/customer_form.html', context)

@login_required
def admin_social_media_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    social_links = SocialMedia.objects.all()
    
    context = {
        'social_links': social_links,
        'section': 'social_media'
    }
    return render(request, 'rentals/admin/social_media_list.html', context)

@login_required
def admin_add_social_media(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = SocialMediaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Social media link added successfully!')
            return redirect('admin_social_media_list')
    else:
        form = SocialMediaForm()
    
    context = {
        'form': form,
        'title': 'Add Social Media Link',
        'section': 'social_media'
    }
    return render(request, 'rentals/admin/social_media_form.html', context)

@login_required
def admin_edit_social_media(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    social_link = get_object_or_404(SocialMedia, pk=pk)
    
    if request.method == 'POST':
        form = SocialMediaForm(request.POST, instance=social_link)
        if form.is_valid():
            form.save()
            messages.success(request, f'{social_link.get_platform_display()} link updated successfully!')
            return redirect('admin_social_media_list')
    else:
        form = SocialMediaForm(instance=social_link)
    
    context = {
        'form': form,
        'social_link': social_link,
        'title': f'Edit {social_link.get_platform_display()} Link',
        'section': 'social_media'
    }
    return render(request, 'rentals/admin/social_media_form.html', context)

@login_required
def admin_delete_social_media(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    social_link = get_object_or_404(SocialMedia, pk=pk)
    
    if request.method == 'POST':
        platform_name = social_link.get_platform_display()
        social_link.delete()
        messages.success(request, f'{platform_name} link deleted successfully!')
        return redirect('admin_social_media_list')
    
    context = {
        'social_link': social_link,
        'section': 'social_media'
    }
    return render(request, 'rentals/admin/social_media_confirm_delete.html', context)

@login_required
def admin_faqs_list(request):
    if not request.user.is_staff:
        return redirect('home')
    
    faqs = FAQ.objects.all()
    
    context = {
        'faqs': faqs,
        'section': 'faqs'
    }
    return render(request, 'rentals/admin/faqs_list.html', context)

@login_required
def admin_add_faq(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ added successfully!')
            return redirect('admin_faqs_list')
    else:
        form = FAQForm()
    
    context = {
        'form': form,
        'title': 'Add New FAQ',
        'section': 'faqs'
    }
    return render(request, 'rentals/admin/faq_form.html', context)

@login_required
def admin_edit_faq(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, 'FAQ updated successfully!')
            return redirect('admin_faqs_list')
    else:
        form = FAQForm(instance=faq)
    
    context = {
        'form': form,
        'faq': faq,
        'title': f'Edit FAQ: {faq.question}'
    }
    return render(request, 'rentals/admin/faq_form.html', context)

@login_required
def admin_delete_faq(request, pk):
    if not request.user.is_staff:
        return redirect('home')
    
    faq = get_object_or_404(FAQ, pk=pk)
    
    if request.method == 'POST':
        faq_question = faq.question
        faq.delete()
        messages.success(request, f'FAQ "{faq_question}" has been deleted successfully!')
        return redirect('admin_faqs_list')
    
    context = {
        'faq': faq,
        'section': 'faqs'
    }
    return render(request, 'rentals/admin/faq_confirm_delete.html', context)