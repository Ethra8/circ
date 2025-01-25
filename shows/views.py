from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Show
from .forms import ShowForm


def show_list(request):
    # Fetch all shows from the database
    shows = Show.objects.all().order_by('time')  # Order by time (upcoming first)
    return render(request, 'shows/show_list.html', {'shows': shows})


def show_details(request, show_id):
    # Fetch the show by ID or return a 404 if it doesn't exist
    show = get_object_or_404(Show, id=show_id)
    return render(request, 'shows/show_details.html', {'show': show})


@login_required
def add_show(request):
    if not request.user.is_superuser:
        messages.error(request, 'Solamente los usuarios de la administración pueden añadir un evento.')
        return redirect(reverse('shows:show_list'))

    if request.method == 'POST':
        # Include request.FILES for file upload (e.g., show image)
        form = ShowForm(request.POST, request.FILES)
        if form.is_valid():
            show = form.save()  # Save the new show instance
            messages.success(request, "Has creado un nuevo Evento!")
            # Redirect without args; assume 'shows:show_list' points to a list view
            return redirect(reverse('shows:show_list'))
        else:
            messages.error(request, "Error al crear el nuevo Evento.")
    else:
        form = ShowForm()

    template = 'shows/add_show.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_show(request, show_id):
    """Edit an existing show."""
    show = get_object_or_404(Show, id=show_id)

    if request.method == 'POST':
        form = ShowForm(request.POST, request.FILES, instance=show)
        if form.is_valid():
            form.save()
            messages.success(request, f"El Evento '{show.name}' ha sido actualizado!")
            return redirect('shows:show_details', show_id=show.id)
        else:
            messages.error(request, "Error al actualizar el Evento. Corrige los siguientes errores.")
    else:
        form = ShowForm(instance=show)

    return render(request, 'shows/edit_show.html', {'form': form, 'show': show})


@login_required
def delete_show(request, show_id):
    """Prompt user to confirm deletion and delete show if confirmed"""
    # Check if the user is an admin or superuser
    if not request.user.is_superuser:
        messages.error(request, 'Solamente los usuarios de la administración pueden borrar un evento.')
        return redirect(reverse('home'))

    # Get the show or return a 404 if not found
    show = get_object_or_404(Show, pk=show_id)

    # If POST request and confirmation is 'Confirm', delete the show
    if request.method == 'POST' and 'confirm_delete' in request.POST:
        show.delete()
        messages.success(request, f'El Evento "{show.name}" se ha eliminado permanentemente.')
        return redirect(reverse('shows:show_list'))

    # If POST request and confirmation is 'Keep', redirect to show details
    elif request.method == 'POST' and 'cancel_delete' in request.POST:
        messages.info(request, f'El Evento "{show.name}" no se ha eliminado, se ha guardado.')
        return redirect(reverse('shows:show_details', args=[show.id]))

    # Render confirmation page
    template = 'shows/delete_confirmation.html'
    context = {
        'show': show,
    }
    return render(request, template, context)

