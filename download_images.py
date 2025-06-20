import os
import requests
import time

def download_image(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded: {filename}")
        return True
    except Exception as e:
        print(f"Error downloading {filename}: {e}")
        return False

def main():
    # Create directories if they don't exist
    directories = [
        'static/images/backgrounds',
        'static/images/cars',
        'static/images/features',
        'static/images/testimonials',
        'static/images/logos'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    # List of image files and their URLs
    images = [
        # Existing images
        ('static/images/backgrounds/hero-bg.jpg', 
         'https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'),
        ('static/images/backgrounds/cta-bg.jpg', 
         'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80'),
        ('static/images/cars/mercedes.jpg', 
         'https://images.unsplash.com/photo-1553440569-bcc63803a83d?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/audi.jpg', 
         'https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/bmw.jpg', 
         'https://images.unsplash.com/photo-1555215695-3004980ad54e?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/porsche.jpg', 
         'https://images.unsplash.com/photo-1503376780353-7e6692767b70?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/hero-car.jpg', 
         'https://images.unsplash.com/photo-1580273916550-e323be2ae537?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80'),
        ('static/images/features/premium-fleet.jpg', 
         'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/features/24-7-support.jpg', 
         'https://images.unsplash.com/photo-1560264280-88b68371db39?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/features/insurance.jpg', 
         'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/features/flexible-pickup.jpg', 
         'https://images.unsplash.com/photo-1604357209793-fca5dca89f97?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        
        # New testimonial images
        ('static/images/testimonials/person1.jpg', 
         'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'),
        ('static/images/testimonials/person2.jpg', 
         'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'),
        ('static/images/testimonials/person3.jpg', 
         'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-4.0.3&auto=format&fit=crop&w=300&q=80'),
        
        # Partner logos
        ('static/images/logos/logo1.png', 
         'https://placehold.co/200x80/4C7BFD/FFFFFF.png?text=Partner+1'),
        ('static/images/logos/logo2.png', 
         'https://placehold.co/200x80/4C7BFD/FFFFFF.png?text=Partner+2'),
        ('static/images/logos/logo3.png', 
         'https://placehold.co/200x80/4C7BFD/FFFFFF.png?text=Partner+3'),
        ('static/images/logos/logo4.png', 
         'https://placehold.co/200x80/4C7BFD/FFFFFF.png?text=Partner+4'),
        
        # Additional car images
        ('static/images/cars/luxury-sedan.jpg', 
         'https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/suv.jpg', 
         'https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        ('static/images/cars/sports-car.jpg', 
         'https://images.unsplash.com/photo-1525609004556-c46c7d6cf023?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'),
        
        # Additional background
        ('static/images/backgrounds/testimonial-bg.jpg', 
         'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80')
    ]
    
    # Download each image
    for filename, url in images:
        success = download_image(url, filename)
        
        # Add a small delay to avoid rate limiting
        time.sleep(0.5)

if __name__ == "__main__":
    main() 