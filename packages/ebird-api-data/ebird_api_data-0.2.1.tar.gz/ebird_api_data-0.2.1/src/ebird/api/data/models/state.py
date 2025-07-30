from django.db import models
from django.utils.translation import gettext_lazy as _


class State(models.Model):
    class Meta:
        verbose_name = _("state")
        verbose_name_plural = _("states")

    code = models.CharField(
        max_length=6,
        primary_key=True,
        verbose_name=_("code"),
        help_text=_("The code used to identify the state."),
    )

    name = models.TextField(
        verbose_name=_("name"), help_text=_("The name of the state.")
    )

    place = models.TextField(
        verbose_name=_("place"), help_text=_("The hierarchical name of the state.")
    )

    created = models.DateTimeField(
        null=True, auto_now_add=True, help_text=_("When was the record created.")
    )

    def __repr__(self) -> str:
        return str(self.code)

    def __str__(self) -> str:
        return str(self.name)
