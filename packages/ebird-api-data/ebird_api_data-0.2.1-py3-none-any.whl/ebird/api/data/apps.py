from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class Config(AppConfig):
    label = "data"
    name = "ebird.api.data"
    verbose_name = _("Data")
