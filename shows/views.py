from django.shortcuts import render, get_object_or_404
from .models import Show

def show_list(request):
    # Fetch all shows from the database
    shows = Show.objects.all().order_by('time')  # Order by time (upcoming first)
    return render(request, 'shows/show_list.html', {'shows': shows})


def show_details(request, show_id):
    # Fetch the show by ID or return a 404 if it doesn't exist
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'shows/show_details.html', {'show': show})