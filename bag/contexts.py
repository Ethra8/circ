from decimal import Decimal
from django.conf import settings
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
        # Parse the item key to determine the type and ID
        item_type, item_id = item_key.split("-")
        item = None

        if item_type == 'show':
            item = Show.objects.get(id=item_id)
            adult_total = quantities.get('adult', 0) * Decimal(item.price_per_seat_adult)
            reduced_total = quantities.get('reduced', 0) * Decimal(item.price_per_seat_reduction)
            subtotal = adult_total + reduced_total
            grand_total += subtotal
            bag_items.append({
                'type': 'show',
                'item': item,
                'quantity_adult': quantities.get('adult', 0),
                'quantity_reduced': quantities.get('reduced', 0),
                'subtotal': subtotal,
            })
        elif item_type == 'taller':
            item = Taller.objects.get(id=item_id)
            quantity = quantities.get('quantity', 0)
            subtotal = quantity * Decimal(item.price)
            grand_total += subtotal
            bag_items.append({
                'type': 'taller',
                'item': item,
                'quantity': quantity,
                'subtotal': subtotal,
            })

    return {
        'bag_items': bag_items,
        'grand_total': grand_total,
    }
