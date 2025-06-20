// Page Navigation (for demo purposes)
function showPage(pageId) {
    // Hide all pages
    document.getElementById('home-page').style.display = 'none';
    document.getElementById('cars-page').style.display = 'none';
    document.getElementById('about-page').style.display = 'none';
    document.getElementById('contact-page').style.display = 'none';
    
    // Show selected page
    document.getElementById(pageId).style.display = 'block';
}

// Navigation link handlers
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const href = this.getAttribute('href');
            
            if (href === '/') {
                showPage('home-page');
            } else if (href === '/cars/') {
                showPage('cars-page');
            } else if (href === '/about/') {
                showPage('about-page');
            } else if (href === '/contact/') {
                showPage('contact-page');
            }
        });
    });
});

// Contact Form Handler
document.getElementById('contactForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Show success message
    alert('Thank you for your message! We will get back to you soon.');
    this.reset();
});

// Filter Form Handler
function clearFilters() {
    document.getElementById('filterForm').reset();
}

// Smooth scrolling for internal links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to navbar
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
const animatedElements = document.querySelectorAll('.car-card, .testimonial, .timeline-item, .stats-card');
animatedElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'all 0.6s ease';
    observer.observe(el);
});

// Form validation and submission
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        // Basic validation
        const name = this.querySelector('[name="name"]');
        const email = this.querySelector('[name="email"]');
        const message = this.querySelector('[name="message"]');
        
        let isValid = true;
        
        // Remove existing error messages
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        
        if (!name.value.trim()) {
            showError(name, 'Name is required');
            isValid = false;
        }
        
        if (!email.value.trim() || !isValidEmail(email.value)) {
            showError(email, 'Valid email is required');
            isValid = false;
        }
        
        if (!message.value.trim()) {
            showError(message, 'Message is required');
            isValid = false;
        }
        
        if (!isValid) {
            e.preventDefault();
        }
    });
}

// Car filter form
const filterForm = document.getElementById('filterForm');
if (filterForm) {
    // Auto-submit on filter change
    const filterInputs = filterForm.querySelectorAll('select, input');
    filterInputs.forEach(input => {
        if (input.type !== 'submit') {
            input.addEventListener('change', function() {
                // Add a small delay to allow for multiple quick changes
                clearTimeout(this.filterTimeout);
                this.filterTimeout = setTimeout(() => {
                    filterForm.submit();
                }, 300);
            });
        }
    });
}

// Mobile sidebar toggle
const sidebarToggle = document.getElementById('sidebarToggle');
const sidebar = document.querySelector('.admin-sidebar');

if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', function() {
        sidebar.classList.toggle('show');
    });
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('show');
            }
        }
    });
}

// Car image upload preview
const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
imageInputs.forEach(input => {
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                // Find or create preview element
                let preview = input.parentNode.querySelector('.image-preview');
                if (!preview) {
                    preview = document.createElement('img');
                    preview.className = 'image-preview mt-2';
                    preview.style.maxWidth = '200px';
                    preview.style.height = 'auto';
                    preview.style.borderRadius = '10px';
                    input.parentNode.appendChild(preview);
                }
                preview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
});

// Car availability toggle
const availabilityToggles = document.querySelectorAll('.availability-toggle');
availabilityToggles.forEach(toggle => {
    toggle.addEventListener('change', function() {
        const carId = this.dataset.carId;
        const status = this.checked ? 'available' : 'rented';
        
        // Send AJAX request to update availability
        fetch(`/api/cars/${carId}/availability/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ status: status })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast('Availability updated successfully', 'success');
            } else {
                showToast('Error updating availability', 'error');
                this.checked = !this.checked; // Revert toggle
            }
        })
        .catch(error => {
            showToast('Error updating availability', 'error');
            this.checked = !this.checked; // Revert toggle
        });
    });
});

// Initialize tooltips
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Initialize popovers
const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl);
});

// Utility functions
function showError(input, message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message text-danger mt-1';
    errorDiv.textContent = message;
    input.parentNode.appendChild(errorDiv);
    input.classList.add('is-invalid');
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // Create toast
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();

    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Search functionality with debounce
function setupSearch() {
    const searchInputs = document.querySelectorAll('.search-input');
    
    searchInputs.forEach(input => {
        let searchTimeout;
        
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            searchTimeout = setTimeout(() => {
                if (query.length >= 2 || query.length === 0) {
                    performSearch(query);
                }
            }, 300);
        });
    });
}

function performSearch(query) {
    // This would typically make an AJAX request to search endpoint
    console.log('Searching for:', query);
}

// Initialize search when DOM is loaded
document.addEventListener('DOMContentLoaded', setupSearch);
