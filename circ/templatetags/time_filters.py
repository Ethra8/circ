from django import template

register = template.Library()

@register.filter
def localized_time(value, language):
    """
    Formats the time based on the user's language.
    - 24-hour format for 'es' and 'fr'
    - AM/PM format for 'en'
    """
    if language in ['es', 'fr']:
        return value.strftime('%H:%M')  # 24-hour format
    return value.strftime('%I:%M %p')  # AM/PM format
