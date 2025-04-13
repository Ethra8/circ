import os
from django.conf import settings

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Value, CharField

from itertools import chain

from shows.models import Show
from tallers.models import Taller


from .models import AboutSection, CompanyContact, Subscription, ContactRequest
from .forms import CompanyContactForm, SubscriptionForm, ContactForm



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


def about(request):
    """ A view to return the about page """
    about_content = AboutSection.objects.first()  # Get the first (and only) AboutSection instance
    return render(request, 'home/about.html', {'about_content': about_content})


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



def contact(request):
    """A view to handle the contact page and its form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')  # Optional success page
    else:
        form = ContactForm()
    return render(request, 'home/contact.html', {'form': form})



def search_results(request):
    """
    Query within all fields of Shows & Tallers for words included
    by user in the navbar's search bar.
    Combines results from both models, identifying their types.
    """
    query = request.GET.get('q', '').strip().lower()  # Normalize query to lowercase

    # Map query terms for audience fields
    audience_mapping = {
        'niños': 'todo_publico',
        'niño': 'todo_publico',
        'adultos': 'todo_publico',
        'adulto': 'todo_publico',
    }

    # Replace query with mapped value if it matches audience terms
    mapped_query = audience_mapping.get(query, query)

    if query:
        # Filter shows by all relevant fields
        show_results = Show.objects.filter(
            Q(name__icontains=query) |  # Use original query for name
            Q(description__icontains=query) |  # Use original query for description
            Q(audience__icontains=query) |  # Include original query
            Q(audience__icontains='todo_publico') |  # Explicitly include 'todo_publico'
            Q(circ_category__icontains=query) |  # Use original query for category
            Q(location_name__icontains=query) |  # Use original query for location name
            Q(location_city__icontains=query)  # Use original query for location city
        )

        # Filter tallers by all relevant fields
        taller_results = Taller.objects.filter(
            Q(name__icontains=query) |  # Use original query for name
            Q(description__icontains=query) |  # Use original query for description
            Q(audience__icontains=query) |  # Include original query
            Q(audience__icontains='todo_publico') |  # Explicitly include 'todo_publico'
            Q(circ_category__icontains=query) |  # Use original query for category
            Q(location_name__icontains=query) |  # Use original query for location name
            Q(location_city__icontains=query)  # Use original query for location city
        )
    else:
        # Return empty results if no query
        show_results = Show.objects.none()
        taller_results = Taller.objects.none()

    # Annotate results with their type
    show_results = show_results.annotate(type=Value('show', output_field=CharField()))
    taller_results = taller_results.annotate(type=Value('taller', output_field=CharField()))

    # Combine results
    combined_results = list(chain(show_results, taller_results))

    # Context for template
    context = {
        'query': query,
        'results': combined_results,  # Unified results with type field
    }

    print("Query:", query)  # Debugging
    print("Mapped Query:", mapped_query)  # Debugging
    print("Number of results:", len(combined_results))  # Debugging

    return render(request, 'home/search_results.html', context)
