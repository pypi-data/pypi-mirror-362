import json

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class TranslationTextInput(forms.MultiWidget):
    template_name = "data/widgets/translation_field.html"

    def __init__(self, *args, **kwargs):
        widgets = [
            forms.TextInput(attrs={"locale": _(language), "class": "vTextField"})
            for code, language in settings.LANGUAGES
        ]
        super().__init__(widgets, **kwargs)

    def decompress(self, value):
        if value:
            data = json.loads(value)
            return [data.get(code, "") for code, language in settings.LANGUAGES]
        return []


class TranslationTextarea(forms.MultiWidget):
    template_name = "data/widgets/translation_field.html"

    def __init__(self, *args, **kwargs):
        if "widgets" not in kwargs:
            kwargs["widgets"] = [
                forms.Textarea(
                    attrs={
                        "locale": _(language),
                        "rows": 10,
                        "class": "vLargeTextField",
                    }
                )
                for code, language in settings.LANGUAGES
            ]
        super().__init__(**kwargs)

    def decompress(self, value):
        if value:
            data = json.loads(value)
            return [data.get(code, "") for code, language in settings.LANGUAGES]
        return []
