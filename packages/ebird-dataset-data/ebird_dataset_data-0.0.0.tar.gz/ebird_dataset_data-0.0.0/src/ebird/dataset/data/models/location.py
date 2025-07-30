from django.db import models
from django.utils.translation import gettext_lazy as _

LOCATION_TYPE = {
    "C": _("County"),
    "H": _("Hotspot"),
    "P": _("Personal"),
    "PC": _("Postal/Zip Code"),
    "S": _("State"),
    "T": _("Town"),
}


class Location(models.Model):
    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the location."),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When was the record created."),
    )

    type = models.TextField(
        blank=True,
        verbose_name=_("type"),
        help_text=_("The location type, e.g. personal, hotspot, town, etc."),
    )

    name = models.TextField(
        verbose_name=_("name"),
        help_text=_("The name of the location."),
    )

    county = models.TextField(
        blank=True,
        verbose_name=_("county"),
        help_text=_("The name of the county (subnational2)."),
    )

    county_code = models.TextField(
        blank=True,
        db_index=True,
        verbose_name=_("county code"),
        help_text=_("The code used to identify the county."),
    )

    state = models.TextField(
        verbose_name=_("state"), help_text=_("The name of the state (subnational1).")
    )

    state_code = models.TextField(
        db_index=True,
        verbose_name=_("state code"),
        help_text=_("The code used to identify the state."),
    )

    country = models.TextField(
        verbose_name=_("country"), help_text=_("The name of the country.")
    )

    country_code = models.TextField(
        db_index=True,
        verbose_name=_("country code"),
        help_text=_("The code used to identify the country."),
    )

    iba_code = models.TextField(
        blank=True,
        verbose_name=_("IBA code"),
        help_text=_("The code used to identify an Important Bird Area."),
    )

    bcr_code = models.TextField(
        blank=True,
        verbose_name=_("BCR code"),
        help_text=_("The code used to identify a Bird Conservation Region."),
    )

    usfws_code = models.TextField(
        blank=True,
        verbose_name=_("USFWS code"),
        help_text=_("The code used to identify a US Fish & Wildlife Service region."),
    )

    atlas_block = models.TextField(
        blank=True,
        verbose_name=_("atlas block"),
        help_text=_("The code used to identify an area for an atlas."),
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

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return str(self.name)
