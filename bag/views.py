from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.shortcuts import get_object_or_404, HttpResponse
from django.contrib import messages
from shows.models import Show


def view_bag(request):
    """A view that renders the bag contents page."""
    bag = request.session.get('bag', {})
    bag_items = []
    grand_total = 0

    for show_id, details in bag.items():
        # Convert show_id back to integer for querying
        show = get_object_or_404(Show, id=int(show_id))
        adult_subtotal = details['adult'] * show.price_per_seat_adult
        reduced_subtotal = details['reduced'] * show.price_per_seat_reduction
        subtotal = adult_subtotal + reduced_subtotal
        grand_total += subtotal

        bag_items.append({
            'show': show,
            'quantity_adult': details['adult'],
            'quantity_reduced': details['reduced'],
            'subtotal': subtotal,
        })

    context = {
        'bag_items': bag_items,
        'grand_total': grand_total,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, show_id):
    """Add a quantity of the specified show to the bag."""
    show = get_object_or_404(Show, id=show_id)
    quantity_adult = int(request.POST.get('quantity_adult', 0))
    quantity_reduced = int(request.POST.get('quantity_reduced', 0))

    # Retrieve or initialize the bag
    bag = request.session.get('bag', {})

    # Ensure show_id is stored as a string
    show_id = str(show_id)

    # Check if the show is already in the bag
    if show_id not in bag:
        bag[show_id] = {'adult': 0, 'reduced': 0}

    # Add quantities
    bag[show_id]['adult'] += quantity_adult
    bag[show_id]['reduced'] += quantity_reduced

    # Save back to session
    request.session['bag'] = bag
    messages.success(request, f'Added tickets for {show.name} to your bag!')
    return redirect('bag:bag')


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the\
    specified amount"""
    print(f"Adjusting item: {item_id}")  # Debug statement
    try:
        show = get_object_or_404(Show, pk=item_id)
        quantity = int(request.POST.get('quantity'))
        bag = request.session.get('bag', {})

        if quantity >= 1:
            bag[item_id] = quantity
            messages.success(request, f'Quantity of\
            {show.name} successfully updated')
        else:
            messages.error(request, f'Failed to update\
            {show.name}')

        request.session['bag'] = bag
        return redirect(reverse('bag'))

    except Exception as e:
        messages.error(request, f'Error updating\
        item: {e}')
        return HttpResponse(status=500)


def remove_bag_item(request, show_id):
    """Remove the item from the shopping bag."""
    try:
        # Access the shopping bag session
        bag = request.session.get('bag', {})

        # Remove the item if it exists
        if str(show_id) in bag:
            del bag[str(show_id)]
            messages.success(request, "Item removed successfully.")
        else:
            messages.warning(request, "Item not found in the bag.")

        # Update the session
        request.session['bag'] = bag
        return redirect('bag:bag')
    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return redirect('bag:bag')
