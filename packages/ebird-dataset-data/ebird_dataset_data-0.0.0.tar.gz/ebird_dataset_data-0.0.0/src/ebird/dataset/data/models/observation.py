from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Observation(models.Model):
    class Meta:
        verbose_name = _("observation")
        verbose_name_plural = _("observations")

    identifier = models.CharField(
        max_length=15,
        primary_key=True,
        verbose_name=_("identifier"),
        help_text=_("The identifier for the observation."),
    )

    created = models.DateTimeField(
        null=True, auto_now_add=True, help_text=_("When was the record created.")
    )

    edited = models.DateTimeField(
        help_text=_("The date and time the observation was last edited"),
        verbose_name=_("edited"),
    )

    checklist = models.ForeignKey(
        "data.Checklist",
        related_name="observations",
        on_delete=models.CASCADE,
        verbose_name=_("checklist"),
        help_text=_("The checklist this observation belongs to."),
    )

    species = models.ForeignKey(
        "data.Species",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("species"),
        help_text=_("The identified species."),
    )

    observer = models.ForeignKey(
        "data.Observer",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("observer"),
        help_text=_("The person who made the observation."),
    )

    location = models.ForeignKey(
        "data.Location",
        related_name="observations",
        on_delete=models.PROTECT,
        verbose_name=_("location"),
        help_text=_("The location where the observation was made."),
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

    count = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name=_("count"),
        help_text=_("The number of birds seen."),
    )

    breeding_code = models.TextField(
        blank=True,
        verbose_name=_("breeding code"),
        help_text=_("eBird code identifying the breeding status."),
    )

    breeding_category = models.TextField(
        blank=True,
        verbose_name=_("breeding category"),
        help_text=_("eBird code identifying the breeding category."),
    )

    behavior_code = models.TextField(
        blank=True,
        verbose_name=_("behaviour code"),
        help_text=_("eBird code identifying the behaviour."),
    )

    age_sex = models.TextField(
        blank=True,
        verbose_name=_("Age & Sex"),
        help_text=_("The number of birds seen in each combination of age and sex."),
    )

    media = models.BooleanField(
        verbose_name=_("has media"),
        help_text=_("Has audio, photo or video uploaded to the Macaulay library."),
    )

    approved = models.BooleanField(
        verbose_name=_("Approved"),
        help_text=_("Has the observation been accepted by eBird's review process."),
    )

    reviewed = models.BooleanField(
        verbose_name=_("Reviewed"),
        help_text=_("Was the observation reviewed because it failed automatic checks."),
    )

    reason = models.TextField(
        blank=True,
        verbose_name=_("Reason"),
        help_text=_(
            "The reason given for the observation to be marked as not confirmed."
        ),
    )

    comments = models.TextField(
        blank=True,
        verbose_name=_("comments"),
        help_text=_("Any comments about the observation."),
    )

    urn = models.TextField(
        blank=True,
        verbose_name=_("URN"),
        help_text=_("The globally unique identifier for the observation."),
    )

    def __repr__(self) -> str:
        return str(self.identifier)

    def __str__(self) -> str:
        return str(self.identifier)
