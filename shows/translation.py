from modeltranslation.translator import register, TranslationOptions
from .models import Show

@register(Show)
class ShowTranslationOptions(TranslationOptions):
    fields = ('description',)