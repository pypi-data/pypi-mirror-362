from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    """
    Location defines the location where the observations in a Checklist
    were made.

    Design Notes
    ------------
    Rather than use country, subnational1 and subnational2 from the eBird API,
    the names country, state and county from the eBird Basic Dataset were used.
    Originally the models were designed so data from either source could be
    loaded, but since the schemas did not overlap completely that meant quite
    a few fields were optional. This dual-purpose role was discarded and the
    models were changed to specifically support the eBird API. The names, state
    and county were kept because they were shorter, and it was easier to remember
    the order.

    The hierarchy: country, state, country describes the administrative, but not
    the geographical/ecological organisation. Being able to identify groups of
    related locations in a national park or Important Bird Areas, or groups of
    counties or states is useful to find out what has been seen in a given area.
    Additional models for Area, Island and Region were considered but ultimately
    rejected for three main reasons:

    1. For hotspots it is easy to map locations to an Area or Island, however
       about 40% of all locations (for Portugal) are personal or private, even
       when the hotspot is well known, or should have been well known. Unless
       these were ignored, that would mean an on-going effort to add these
       locations to the relevant groups. For even a small country or area the
       effort is enormous. Autocorrecting location should be possible but that
       would mean defining boundaries for each hotspot. There was talk of eBird
       doing that but again the effort would be enormous.

    2. If the hierarchy is extended to add new levels, then the codes used by
       eBird, US, US-NY, US-NY-109 would need to be changed to incorporate
       the new levels, since it makes finding related locations easy. The
       alternative is to create the hierarchy using foreign keys. Again that
       create a considerable administrative burden.

    3. Grouping locations, countries, or states is mainly for usability,
       however for small numbers of each, adding form controls that support
       multi-select can be used as a workaround / viable alternative, and
       even provide more flexibility.

    On the second point, it might be worth adopting an alternative hierarchy
    such as the NUTS3 system used in the European Union, which has an extra
    level. It also uses hierarchical codes, e.g. PT1, PT15, PT15D. Counties
    are the smallest areas, and are shared by both systems, so it is easy to
    map eBird codes to NUTS codes.

    Optimisations
    -------------
    A Checklist has a Location, but the hierarchy was flattened so the County,
    State and Country are duplicated on the Checklist model to reduce the
    number of joins, and so speed up queries. Similarly, Location, County, State,
    and Country are duplicated on Observation for the same reason.

    """

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the location."),
    )

    original = models.TextField(
        verbose_name=_("original name"),
        help_text=_("The original name of the location from eBird."),
    )

    name = models.TextField(
        verbose_name=_("name"),
        help_text=_("The display name of the location."),
    )

    country = models.ForeignKey(
        "data.Country",
        related_name="locations",
        on_delete=models.PROTECT,
        verbose_name=_("country"),
        help_text=_("The country for the location."),
    )

    state = models.ForeignKey(
        "data.State",
        related_name="locations",
        on_delete=models.PROTECT,
        verbose_name=_("state"),
        help_text=_("The state for the location."),
    )

    county = models.ForeignKey(
        "data.County",
        blank=True,
        null=True,
        related_name="locations",
        on_delete=models.PROTECT,
        verbose_name=_("county"),
        help_text=_("The county for the location."),
    )

    latitude = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=7,
        max_digits=9,
        verbose_name=_("latitude"),
        help_text=_("The decimal latitude of the location, relative to the equator."),
    )

    longitude = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=7,
        max_digits=10,
        verbose_name=_("longitude"),
        help_text=_(
            "The decimal longitude of the location, relative to the prime meridian."
        ),
    )

    url = models.URLField(
        blank=True,
        verbose_name=_("url"),
        help_text=_("URL of the location page on eBird."),
    )

    hotspot = models.BooleanField(
        blank=True,
        null=True,
        verbose_name=_("is hotspot"),
        help_text=_("Is the location a hotspot."),
    )

    data = models.JSONField(
        verbose_name=_("Data"),
        help_text=_("Data describing a Location."),
        default=dict,
        blank=True,
    )

    created = models.DateTimeField(
        null=True, auto_now_add=True, help_text=_("When was the record created.")
    )

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return self.name
