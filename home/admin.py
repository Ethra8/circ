from django.contrib import admin
from .models import AboutSection
from django_summernote.admin import SummernoteModelAdmin

@admin.register(AboutSection)
class AboutSectionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)