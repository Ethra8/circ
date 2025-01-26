from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from shows.models import Show
from tallers.models import Taller


def view_bag(request):
    """A view that renders the bag contents page."""
    bag = request.session.get('bag', {})
    bag_items = []
    grand_total = 0

    for item_key, details in bag.items():
        item_type, item_id = item_key.split("-")
        item_id = int(item_id)  # Convert back to integer
        item = None

        # Check if the item is a Show or Taller
        if item_type == 'show':
            item = get_object_or_404(Show, id=item_id)
            quantity_adult = details.get('quantity_adult', 0)
            quantity_child = details.get('quantity_child', 0)

            adult_subtotal = quantity_adult * item.price_per_seat_adult
            reduced_subtotal = quantity_child * item.price_per_seat_reduction
            subtotal = adult_subtotal + reduced_subtotal
        elif item_type == 'taller':
            item = get_object_or_404(Taller, id=item_id)
            quantity_adult = details.get('quantity_adult', 0)
            quantity_child = 0  # Tallers don't have reduced tickets

            subtotal = quantity_adult * item.price_per_seat_adult

        # Add item to the bag items list
        bag_items.append({
            'type': item_type,
            'item': item,
            'quantity_adult': quantity_adult,
            'quantity_child': quantity_child,
            'subtotal': subtotal,
        })

        # Add to grand total
        grand_total += subtotal

    context = {
        'bag_items': bag_items,
        'grand_total': grand_total,
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_type, item_id):
    """
    Add a quantity of the specified item to the shopping bag.
    """
    try:
        # Retrieve the session bag
        bag = request.session.get('bag', {})

        # Construct the item_key (e.g., "taller-1")
        item_key = f"{item_type}-{item_id}"
        
        # Retrieve the item object
        if item_type == 'taller':
            item = get_object_or_404(Taller, id=item_id)
        elif item_type == 'show':
            item = get_object_or_404(Show, id=item_id)
        else:
            messages.error(request, "Invalid item type.")
            return redirect('bag:bag')

        # Retrieve quantities from POST data
        quantity_adult = int(request.POST.get('quantity_adult', 0))
        quantity_child = int(request.POST.get('quantity_child', 0))

        # Initialize or update the item in the bag
        if item_key not in bag:
            bag[item_key] = {
                'type': item_type,
                'quantity_adult': quantity_adult,
                'quantity_child': quantity_child,
            }
        else:
            bag[item_key]['quantity_adult'] += quantity_adult
            bag[item_key]['quantity_child'] += quantity_child

        # Save the updated bag to the session
        request.session['bag'] = bag
        messages.success(request, f"Added {item.name} to your bag!")

    except Exception as e:
        messages.error(request, f"Error adding item to the bag: {e}")

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
            quantity_child = int(request.POST.get('quantity_child', 0))

            if quantity_adult >= 1 or quantity_child >= 1:
                # Update the quantities in the bag
                bag[item_key]['adult'] = quantity_adult
                bag[item_key]['reduced'] = quantity_child
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
    """Remove the specified item (show or taller) from the shopping bag."""
    try:
        # Access the shopping bag session
        bag = request.session.get('bag', {})

        # Construct the item key
        item_key = f"{item_type}-{item_id}"

        # Check if the item exists in the bag
        if item_key in bag:
            del bag[item_key]
            messages.success(request, f"{item_type.capitalize()} removed successfully from the bag.")
        else:
            messages.warning(request, "Item not found in the bag.")

        # Update the session
        request.session['bag'] = bag
        return redirect('bag:bag')

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return redirect('bag:bag')
