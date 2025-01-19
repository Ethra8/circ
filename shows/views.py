from django.shortcuts import render
from .models import Show

def show_list(request):
    # Fetch all shows from the database
    shows = Show.objects.all().order_by('time')  # Order by time (upcoming first)
    return render(request, 'shows/show_list.html', {'shows': shows})