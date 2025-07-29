import json

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .widgets import TranslationTextarea, TranslationTextInput


class TranslationField(forms.MultiValueField):
    def __init__(self, **kwargs):
        # Define one set of messages for all fields.
        kwargs["error_messages"] = {
            "required": "Enter the text for the translation",
            "incomplete": "Enter text for every translation",
        }
        super().__init__(require_all_fields=True, **kwargs)

    def compress(self, data_list):
        codes = [code for code, language in settings.LANGUAGES]
        values = zip(codes, data_list)
        translations = {code: value for code, value in values}
        return json.dumps(translations)

    def has_changed(self, initial, data):
        # If the value from the database is an empty string, rather than
        # the string representation of an empty dict, set the value to None,
        # so it decompresses correctly.
        return super().has_changed(initial or None, data)


class TranslationCharField(TranslationField):
    def __init__(self, **kwargs):
        fields = [
            forms.CharField(label=_(language)) for code, language in settings.LANGUAGES
        ]
        widget = TranslationTextInput
        super().__init__(fields=fields, widget=widget, **kwargs)


class TranslationTextField(TranslationField):
    def __init__(self, **kwargs):
        fields = [
            forms.CharField(label=_(language)) for code, language in settings.LANGUAGES
        ]
        widget = TranslationTextarea
        super().__init__(fields=fields, widget=widget, **kwargs)
