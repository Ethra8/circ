from django.contrib import admin
from .models import AboutSection, ContactRequest, GalleryImage
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


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title', 'caption', 'alt_text')