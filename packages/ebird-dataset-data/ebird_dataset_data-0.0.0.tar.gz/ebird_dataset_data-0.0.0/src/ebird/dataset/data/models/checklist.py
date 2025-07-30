from django.db import models
from django.utils.translation import gettext_lazy as _

# All the protocols from Appendices 2 and 3 of the eBird Basic Dataset
# Metadata V1.14 description.

PROTOCOL_TYPE = {
    "P22": _("Travelling"),
    "P21": _("Stationary"),
    "P62": _("Historical"),
    "P20": _("Incidental"),
    "P23": _("Area"),
    "P33": _("Banding"),
    "P60": _("Pelagic"),
    "P54": _("Nocturnal Flight Call Count"),
    "P52": _("Oiled Birds"),
    "P48": _("Random"),
    "P59": _("TNC California Waterbird Count"),
    "P46": _("CWC Point Count"),
    "P47": _("CWC Area Search"),
    "P80": _("CWC Travelling Count"),
    "P41": _("Rusty Blackbird Spring Migration Blitz"),
    "P69": _("California Brown Pelican Survey"),
    "P73": _("PROALAS Point Count (2 Bands)"),
    "P81": _("PROALAS Mini-transect"),
    "P82": _("PROALAS Point Count (3 Bands)"),
    "P83": _("Orange-breasted Falcon Site Survey"),
    "P58": _("Audubon Coastal Bird Survey"),
    "P74": _("International Shorebird Survey"),
    "P84": _("Migratory Shorebird Protocol"),
    "P70": _("BirdLife Australia 20min-2ha survey"),
    "P72": _("BirdLife Australia 5 km radius search"),
    "P71": _("BirdLife Australia 500m radius search"),
    "P66": _("Birds 'n' Bogs Survey"),
    "P65": _("Breeding Bird Atlas"),
    "P67": _("Common Bird Survey"),
    "P50": _("Caribbean Martin Survey"),
    "P49": _("Coastal Shorebird Survey"),
    "P57": _("Great Texas Birding Classic"),
    "P51": _("Greater Gulf Refuge Waterbird Count"),
    "P56": _("Heron Area Count"),
    "P55": _("Heron Stationary Count"),
    "P61": _("IBA Canada"),
    "P39": _("LoonWatch"),
    "P35": _("My Yard Counts"),
    "P68": _("RAM--Iberian Seawatch Network"),
    "P40": _("Standardized Yard Count"),
    "P30": _("Trail Tracker"),
    "P75": _("Tricolored Blackbird Winter Survey"),
    "P64": _("Traveling - Property Specific"),
    "P34": _("Waterbird Count"),
    "P44": _("Yellow-billed Magpie Survey - General Observations"),
    "P45": _("Yellow-billed Magpie Survey - Traveling Count"),
}


class Checklist(models.Model):
    class Meta:
        verbose_name = _("checklist")
        verbose_name_plural = _("checklists")

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The unique identifier for the checklist."),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When was the record created."),
    )

    edited = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_("The date and time the eBird checklist was last edited."),
        verbose_name=_("edited"),
    )

    location = models.ForeignKey(
        "data.Location",
        related_name="checklists",
        on_delete=models.PROTECT,
        verbose_name=_("location"),
        help_text=_("The location where checklist was made."),
    )

    county_code = models.TextField(
        blank=True,
        db_index=True,
        verbose_name=_("county code"),
        help_text=_("The code used to identify the county."),
    )

    state_code = models.TextField(
        db_index=True,
        verbose_name=_("state code"),
        help_text=_("The code used to identify the state."),
    )

    country_code = models.TextField(
        db_index=True,
        verbose_name=_("country code"),
        help_text=_("The code used to identify the country."),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="checklists",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who submitted the checklist."),
    )

    group = models.TextField(
        blank=True,
        verbose_name=_("group"),
        help_text=_("The identifier for a group of observers."),
    )

    observer_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("observer count"),
        help_text=_("The total number of observers."),
    )

    species_count = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("species count"),
        help_text=_("The number of species reported."),
    )

    date = models.DateField(
        db_index=True,
        verbose_name=_("date"),
        help_text=_("The date the observations were made."),
    )

    time = models.TimeField(
        blank=True,
        null=True,
        verbose_name=_("time"),
        help_text=_("The time the observations were made."),
    )

    started = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
        verbose_name=_("date & time"),
        help_text=_("The date and time the observations were made."),
    )

    protocol = models.TextField(
        blank=True,
        verbose_name=_("protocol"),
        help_text=_("The protocol followed, e.g. travelling, stationary, etc."),
    )

    protocol_code = models.TextField(
        blank=True,
        verbose_name=_("protocol code"),
        help_text=_("The code used to identify the protocol."),
    )

    project_code = models.TextField(
        blank=True,
        verbose_name=_("project code"),
        help_text=_("The code used to identify the project (portal)."),
    )

    duration = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_("duration"),
        help_text=_("The number of minutes spent counting."),
    )

    distance = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=3,
        max_digits=6,
        verbose_name=_("distance"),
        help_text=_("The distance, in metres, covered while travelling."),
    )

    area = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=3,
        max_digits=6,
        verbose_name=_("area"),
        help_text=_("The area covered, in hectares."),
    )

    complete = models.BooleanField(
        default=False,
        verbose_name=_("complete"),
        help_text=_("All species seen are reported."),
    )

    comments = models.TextField(
        blank=True,
        verbose_name=_("comments"),
        help_text=_("Any comments about the checklist."),
    )

    url = models.URLField(
        blank=True,
        verbose_name=_("url"),
        help_text=_("URL where the original checklist can be viewed."),
    )

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return str(self.identifier)
