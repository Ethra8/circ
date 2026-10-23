from modeltranslation.translator import register, TranslationOptions
from .models import AboutSection

@register(AboutSection)
class AboutTranslationOptions(TranslationOptions):
    fields = ('content',)