from decimal import Decimal
from django.conf import settings
from shows.models import Show

def bag_contents(request):
    """
    Make bag items and grand total available across all templates.
    """
    bag = request.session.get('bag', {})
    grand_total = Decimal('0.00')

    for show_id, quantities in bag.items():
        adult_total = quantities.get('adult', 0) * Decimal(quantities.get('price_per_seat_adult', 0))
        reduced_total = quantities.get('reduced', 0) * Decimal(quantities.get('price_per_seat_reduction', 0))
        grand_total += adult_total + reduced_total

    return {
        'grand_total': grand_total,
    }