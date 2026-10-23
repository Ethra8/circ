from modeltranslation.translator import register, TranslationOptions
from .models import Taller

@register(Taller)
class TallerTranslationOptions(TranslationOptions):
    fields = ('description',)