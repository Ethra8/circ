from decimal import Decimal
from django.shortcuts import get_object_or_404
from shows.models import Show
from tallers.models import Taller

def bag_contents(request):
    """
    Make bag items and grand total available across all templates.
    """
    bag = request.session.get('bag', {})
    bag_items = []
    grand_total = Decimal('0.00')

    for item_key, quantities in bag.items():
        try:
            # Parse the item key to determine the type and ID
            item_type, item_id = item_key.split("-")
            item = None

            # Fetch the corresponding item (Show or Taller)
            if item_type == 'show':
                item = get_object_or_404(Show, id=item_id)
            elif item_type == 'taller':
                item = get_object_or_404(Taller, id=item_id)

            # Retrieve quantities
            quantity_adult = quantities.get('quantity_adult', 0)
            quantity_reduced = quantities.get('quantity_reduced', 0)

            # Calculate totals
            adult_total = quantity_adult * Decimal(item.price_per_seat_adult)
            reduced_total = quantity_reduced * Decimal(item.price_per_seat_reduction)
            subtotal = adult_total + reduced_total
            grand_total += subtotal

            # Append the item details to bag_items
            bag_items.append({
                'type': item_type,  # 'show' or 'taller'
                'item': item,
                'quantity_adult': quantity_adult,
                'quantity_reduced': quantity_reduced,
                'subtotal': subtotal,
            })

        except Exception as e:
            print(f"Error processing bag item {item_key}: {e}")

    return {
        'bag_items': bag_items,
        'grand_total': grand_total,
    }
