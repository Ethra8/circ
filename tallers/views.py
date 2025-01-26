from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from shows.models import Show
from .forms import TallerForm
from .models import Taller


def taller_list(request):
    # Fetch all tallers from the database
    tallers = Taller.objects.all().order_by('starting_date')  # Order by dates (upcoming first)
    return render(request, 'tallers/taller_list.html', {'tallers': tallers})


def taller_details(request, taller_id):
    # Fetch the taller by ID or return a 404 if it doesn't exist
    taller = get_object_or_404(Taller, id=taller_id)
    return render(request, 'tallers/taller_details.html', {'taller': taller})


@login_required
def add_taller(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes acceso para realizar esta acción. Solamente los administradores del sitio pueden añadir talleres.')
        return redirect(reverse('tallers:taller_list'))

    if request.method == 'POST':
        # Include request.FILES for file upload (e.g., taller's image)
        form = TallerForm(request.POST, request.FILES)
        if form.is_valid():
            taller = form.save()  # Save the new taller instance
            messages.success(request, "Has creado un nuevo Taller!")
            # Redirect without args; assume 'tallers:taller_list' points to a list view
            return redirect(reverse('tallers:taller_list'))
        else:
            messages.error(request, "Error al crear el nuevo Taller.")
    else:
        form = TallerForm()

    template = 'tallers/add_taller.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_taller(request, taller_id):
    """Edit an existing taller."""
    taller = get_object_or_404(Taller, id=taller_id)

    if request.method == 'POST':
        form = TallerForm(request.POST, request.FILES, instance=taller)
        if form.is_valid():
            form.save()
            messages.success(request, f"El Taller '{taller.name}' ha sido actualizado!")
            return redirect('tallers:taller_details', taller_id=taller.id)
        else:
            messages.error(request, "Error al actualizar taller. Por favor, corrige los siguientes errores.")
    else:
        form = TallerForm(instance=taller)

    return render(request, 'tallers/edit_taller.html', {'form': form, 'taller': taller})


@login_required
def delete_taller(request, taller_id):
    """Prompt user to confirm deletion and delete taller if confirmed"""
    # Check if the user is an admin or superuser
    if not request.user.is_superuser:
        messages.error(request, 'No tienes acceso para realizar esta acción. Solamente los administradores del sitio pueden cancelar talleres.')
        return redirect(reverse('home'))

    # Get the taller or return a 404 if not found
    taller = get_object_or_404(Taller, pk=taller_id)

    # If POST request and confirmation is 'Confirm', delete the taller
    if request.method == 'POST' and 'confirm_delete' in request.POST:
        taller.delete()
        messages.success(request, f'El Taller "{taller.name}" se ha eliminado permanentemente.')
        return redirect(reverse('tallers:taller_list'))

    # If POST request and confirmation is 'Keep', redirect to taller details
    elif request.method == 'POST' and 'cancel_delete' in request.POST:
        messages.info(request, f'No se ha eliminado el Taller "{taller.name}"')
        return redirect(reverse('tallers:taller_details', args=[taller.id]))

    # Render confirmation page
    template = 'tallers/delete_confirmation.html'
    context = {
        'taller': taller,
    }
    return render(request, template, context)


def book_taller(request, taller_id):
    """User books a taller,
    if taller is fully booked, returns warning.
    """

    taller = get_object_or_404(Taller, id=taller_id)

    try:
        taller.book_participant()
        messages.success(request, f"Tu plaza está reservada para el Taller: '{taller.name}'!")
    except ValueError as e:
        messages.warning(request, f"El Taller '{taller.name}' está completo. Missed requests count: {taller.users_missed_requests}")

    return redirect('taller_detail', taller_id=taller.id)


def search_results(request):
    """
    Query within descriptions of Shows & Tallers for words included
    by user in navbar's search bar
    """

    query = request.GET.get('q', '')
    show_results = Show.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Show.objects.none()
    taller_results = Taller.objects.filter(Q(name__icontains=query) | Q(description__icontains=query)) if query else Taller.objects.none()

    context = {
        'query': query,
        'show_results': show_results,
        'taller_results': taller_results,
    }
    return render(request, 'tallers/search_results.html', context)
