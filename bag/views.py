from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from django.contrib import messages
from django.http import Http404

from shows.models import Show
from tallers.models import Taller


def view_bag(request):
    """Render the shopping bag page."""
    bag = request.session.get('bag', {})
    bag_items = []
    grand_total = 0  # Initialize the grand total

    for item_key, details in bag.items():
        try:
            # Split the key to get item_type and item_id
            item_type, item_id = item_key.split('-')
            if item_type == 'taller':
                item = Taller.objects.get(id=item_id)
            elif item_type == 'show':
                item = Show.objects.get(id=item_id)
            else:
                continue  # Skip unknown item types

            # Calculate the subtotal for this item
            subtotal_adult = details['adult'] * float(item.price_per_seat_adult)
            subtotal_child = details['child'] * float(item.price_per_seat_reduction or 0)
            subtotal = subtotal_adult + subtotal_child

            # Add the subtotal to the grand total
            grand_total += subtotal

            # Append each item with its details to bag_items
            bag_items.append({
                'type': item_type,  # item.type will be available in the template
                'item': item,       # item.item.id will resolve to the item ID
                'quantity_adult': details['adult'],
                'quantity_child': details['child'],
                'subtotal_adult': subtotal_adult,
                'subtotal_child': subtotal_child,
                'subtotal': subtotal,
            })
        except (Taller.DoesNotExist, Show.DoesNotExist):
            # Handle cases where items might not exist
            print(f"Error processing bag item {item_key}: Item not found.")
            continue

    context = {
        'bag_items': bag_items,
        'grand_total': grand_total,  # Pass the grand total to the template
    }
    return render(request, 'bag/bag.html', context)


def add_to_bag(request, item_type, item_id):
    """Add a quantity of the specified item to the shopping bag."""
    # Validate item_type and retrieve the object
    if item_type == 'taller':
        try:
            item = Taller.objects.get(id=item_id)
        except Taller.DoesNotExist:
            raise Http404("Taller not found.")
    elif item_type == 'show':
        try:
            item = Show.objects.get(id=item_id)
        except Show.DoesNotExist:
            raise Http404("Show not found.")
    else:
        raise Http404("Invalid item type.")

    # Retrieve quantities from the POST request
    quantity_adult = int(request.POST.get('quantity_adult', 0))
    quantity_child = int(request.POST.get('quantity_child', 0))

    # Ensure at least one quantity is provided
    if quantity_adult <= 0 and quantity_child <= 0:
        messages.error(request, "Please add at least one ticket.")
        return redirect('bag:bag')

    # Retrieve or initialize the shopping bag
    bag = request.session.get('bag', {})

    # Create a unique key for the item
    item_key = f"{item_type}-{item_id}"

    # Update or add the item to the bag
    if item_key in bag:
        bag[item_key]['adult'] += quantity_adult
        bag[item_key]['child'] += quantity_child
    else:
        bag[item_key] = {'adult': quantity_adult, 'child': quantity_child, 'name': item.name}

    # Save the updated bag back into the session
    request.session['bag'] = bag

    # Log bag contents for debugging
    print("Bag contents:", request.session['bag'])

    # Success message and redirect
    messages.success(request, f"Added {item.name} to your bag!")
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
