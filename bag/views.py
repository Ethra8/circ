from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from shows.models import Show
from tallers.models import Taller


def view_bag(request):
    """A view that renders the bag contents page."""
    bag = request.session.get('bag', {})
    bag_items = []
    grand_total = 0

    for item_id, details in bag.items():
        # Check if the item is a Show or Taller
        if details.get('type') == 'show':
            item = get_object_or_404(Show, id=int(item_id))
            quantity_adult = details.get('adult', 0)
            quantity_reduced = details.get('reduced', 0)

            adult_subtotal = quantity_adult * item.price_per_seat_adult
            reduced_subtotal = quantity_reduced * item.price_per_seat_reduction
            subtotal = adult_subtotal + reduced_subtotal

            bag_items.append({
                'show': item,
                'taller': None,
                'quantity_adult': quantity_adult,
                'quantity_reduced': quantity_reduced,
                'subtotal': subtotal,
            })
            grand_total += subtotal

        elif details.get('type') == 'taller':
            item = get_object_or_404(Taller, id=int(item_id))
            quantity = details.get('quantity', 0)

            subtotal = quantity * item.price
            bag_items.append({
                'show': None,
                'taller': item,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            grand_total += subtotal

    context = {
        'bag_items': bag_items,
        'grand_total': grand_total,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_type, item_id):
    """Add a quantity of the specified item (show or taller) to the bag."""
    try:
        # Retrieve the item based on type
        if item_type == 'show':
            item = get_object_or_404(Show, id=item_id)
            quantity_adult = int(request.POST.get('quantity_adult', 0))
            quantity_reduced = int(request.POST.get('quantity_reduced', 0))
        elif item_type == 'taller':
            item = get_object_or_404(Taller, id=item_id)
            quantity_adult = int(request.POST.get('quantity', 0))  # For taller, use 'quantity'

        # Retrieve or initialize the bag
        bag = request.session.get('bag', {})

        # Construct a unique key for each item
        item_key = f"{item_type}-{item_id}"

        # Initialize the item in the bag if it doesn't exist
        if item_key not in bag:
            bag[item_key] = {'quantity_adult': 0, 'quantity_reduced': 0} if item_type == 'show' else {'quantity': 0}

        # Update quantities
        if item_type == 'show':
            bag[item_key]['quantity_adult'] += quantity_adult
            bag[item_key]['quantity_reduced'] += quantity_reduced
        elif item_type == 'taller':
            bag[item_key]['quantity'] += quantity_adult  # Add the adult quantity for taller

        # Save back to session
        request.session['bag'] = bag

        # Success message
        messages.success(request, f'Added {quantity_adult} tickets for {item.name} to your bag!')
        return redirect('bag:bag')
    except Exception as e:
        # Error message for unexpected issues
        messages.error(request, f"Error adding item to bag: {e}")
        return redirect('bag:bag')


def adjust_bag(request, item_key):
    """Adjust the quantity of the specified item to the specified amount."""
    try:
        # Split the item key to determine the type and ID
        item_type, item_id = item_key.split("-")
        item = None

        # Determine the type of the item
        if item_type == 'show':
            item = get_object_or_404(Show, id=int(item_id))
        elif item_type == 'taller':
            item = get_object_or_404(Taller, id=int(item_id))
        else:
            raise ValueError("Invalid item type")

        # Retrieve the bag from the session
        bag = request.session.get('bag', {})

        # Adjust quantities for "show" or "taller"
        if item_type == 'show':
            # Get adult and reduced ticket quantities for shows
            quantity_adult = int(request.POST.get('quantity_adult', 0))
            quantity_reduced = int(request.POST.get('quantity_reduced', 0))

            if quantity_adult >= 1 or quantity_reduced >= 1:
                # Update the quantities in the bag
                bag[item_key]['adult'] = quantity_adult
                bag[item_key]['reduced'] = quantity_reduced
                messages.success(
                    request, 
                    f'Quantities for {item.name} successfully updated.'
                )
            else:
                # Remove the item if both quantities are zero
                del bag[item_key]
                messages.success(
                    request, 
                    f'{item.name} removed from the bag.'
                )

        elif item_type == 'taller':
            # Get the single quantity for taller
            quantity = int(request.POST.get('quantity', 0))

            if quantity >= 1:
                # Update the quantity in the bag
                bag[item_key]['quantity'] = quantity
                messages.success(
                    request, 
                    f'Quantity of {item.name} successfully updated.'
                )
            else:
                # Remove the item if quantity is zero
                del bag[item_key]
                messages.success(
                    request, 
                    f'{item.name} removed from the bag.'
                )

        # Save the updated bag back to the session
        request.session['bag'] = bag
        return redirect('bag:bag')

    except Exception as e:
        messages.error(request, f'Error updating item: {e}')
        return HttpResponse(status=500)



# def remove_bag_item(request, item_key):
#     """Remove the item from the shopping bag."""
#     try:
#         bag = request.session.get('bag', {})

#         # Remove the item if it exists
#         if item_key in bag:
#             del bag[item_key]
#             messages.success(request, "Item removed successfully.")
#         else:
#             messages.warning(request, "Item not found in the bag.")

#         # Update the session
#         request.session['bag'] = bag
#         return redirect('bag:bag')

#     except Exception as e:
#         messages.error(request, f"Error removing item: {e}")
#         return redirect('bag:bag')


def remove_bag_item(request, item_type, item_id):
    """Remove the item from the shopping bag."""
    try:
        # Access the shopping bag session
        bag = request.session.get('bag', {})

        # Convert item_id to a string to match the session keys
        item_id = str(item_id)

        # Check the type and remove the item if it exists
        if item_type == 'show' and item_id in bag:
            del bag[item_id]
            messages.success(request, "Show removed successfully.")
        elif item_type == 'taller' and item_id in bag:
            del bag[item_id]
            messages.success(request, "Taller removed successfully.")
        else:
            messages.warning(request, "Item not found in the bag.")

        # Update the session
        request.session['bag'] = bag
        return redirect('bag:bag')

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return redirect('bag:bag')
