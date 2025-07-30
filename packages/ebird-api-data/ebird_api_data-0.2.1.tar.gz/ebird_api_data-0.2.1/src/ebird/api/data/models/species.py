import json
import logging

from json import JSONDecodeError

from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

log = logging.getLogger(__name__)


class Species(models.Model):
    class Category(models.TextChoices):
        ALL = "", _("All categories")
        SPECIES = "species", _("Species")
        SUBSPECIES = "issf", _("Subspecies")
        DOMESTIC = "domestic", _("Domestic")
        HYBRID = "hybrid", _("Hybrid")

    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")

    taxon_order = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("taxonomy order"),
        help_text=_("The position in the eBird/Clements taxonomic order."),
    )

    order = models.TextField(
        blank=True,
        verbose_name=_("order"),
        help_text=_(
            "The order, e.g. Struthioniformes, from the eBird/Clements taxonomy."
        ),
    )

    category = models.TextField(
        blank=True,
        choices=Category,
        verbose_name=_("category"),
        help_text=_("The category from the eBird/Clements taxonomy."),
    )

    species_code = models.CharField(
        max_length=10,
        primary_key=True,
        verbose_name=_("species code"),
        help_text=_("The species code, e.g. ostric2, used in the eBird API."),
    )

    family_code = models.TextField(
        blank=True,
        verbose_name=_("family code"),
        help_text=_("The family code, e.g. struth1, used in the eBird API."),
    )

    common_name = models.TextField(
        verbose_name=_("common name"),
        help_text=_("The species common name in the eBird/Clements taxonomy."),
    )

    scientific_name = models.TextField(
        verbose_name=_("scientific name"),
        help_text=_("The species scientific name in the eBird/Clements taxonomy."),
    )

    family_common_name = models.TextField(
        blank=True,
        verbose_name=_("family common name"),
        help_text=_(
            "The common name for the species family in the eBird/Clements taxonomy."
        ),
    )

    family_scientific_name = models.TextField(
        blank=True,
        verbose_name=_("family scientific name"),
        help_text=_(
            "The scientific name for the species family in the eBird/Clements taxonomy."
        ),
    )

    data = models.JSONField(
        verbose_name=_("Data"),
        help_text=_("Data describing a Species."),
        default=dict,
        blank=True,
    )

    created = models.DateTimeField(
        null=True, auto_now_add=True, help_text=_("When was the record created.")
    )

    def __repr__(self) -> str:
        return str(self.species_code)

    def __str__(self) -> str:
        return self.get_common_name()

    def get_common_name(self) -> str:
        try:
            data = json.loads(self.common_name)
            common_name = data.get(get_language(), "")
            if not common_name:
                common_name = data.get(next(iter(data)), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Species common_name: %s", self.id)
            common_name = ""
        return common_name

    def get_family_common_name(self) -> str:
        try:
            data = json.loads(self.family_common_name)
            family_name = data.get(get_language(), "")
            if not family_name:
                family_name = data.get(next(iter(data)), "")
        except JSONDecodeError:
            log.error("Incorrect JSON for Species family_name: %s", self.id)
            family_name = ""
        return family_name
