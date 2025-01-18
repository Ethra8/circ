import os
from django.conf import settings

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import CompanyContact, Subscription
from .forms import CompanyContactForm, SubscriptionForm


def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')


def gallery(request):
    """
    Lists all images in the media/gallery folder and passes them to the template.
    """
    # Define the folder path
    gallery_folder = os.path.join(settings.MEDIA_ROOT, 'gallery')

    # Get the list of image file paths
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    images = [
        f'media/gallery/{file_name}'
        for file_name in os.listdir(gallery_folder)
        if file_name.lower().endswith(image_extensions)
    ]

    # Pass the image paths to the template
    return render(request, 'home/gallery.html', {'images': images})


# def companies(request):
#     """ A view to return the companies page with form"""

#     form = CompanyContactForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Your message has been sent successfully!')
#         return redirect('companies')
#     form = CompanyContactForm()

#     return render(request, 'home/companies.html', {'form': form})


# def about(request):
#     """ A view to return the about page """
#     return render(request, 'home/about.html')


# def subscribe(request):
#     """ A view to return the subscribe form """
#     if request.method == 'POST':
#         form = SubscriptionForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your subscription has been successfully\
#             registered!')
#             return redirect('home')
#         else:
#             messages.error(request, 'An error has occured, please check\
#             your email, or try again later.')
#         return redirect('subscribe')
#     else:
#         form = SubscriptionForm()
#     return render(request, 'home/subscribe_form.html', {'form': form})


