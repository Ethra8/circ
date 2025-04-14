from django.contrib import admin
from .models import AboutSection, ContactRequest
from django_summernote.admin import SummernoteModelAdmin

@admin.register(AboutSection)
class AboutSectionAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at',)
    search_fields = ('name', 'email')
    readonly_fields = ('submitted_at',)  # Makes it visible in detail view
    # Optional: control which fields show up and in what order
    fields = ('submitted_at', 'name', 'email', 'message')