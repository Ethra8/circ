from django.forms.widgets import ClearableFileInput


class TranslatedFileInput(ClearableFileInput):
    template_name = "widgets/translated_file_input.html"