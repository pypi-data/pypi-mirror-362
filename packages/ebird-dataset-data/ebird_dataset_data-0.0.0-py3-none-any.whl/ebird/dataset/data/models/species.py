from django.db import models
from django.utils.translation import gettext_lazy as _


SPECIES_CATEGORY = {
    "species": _("Species"),
    "sub-species": _("Sub-species"),
    "hybrid": _("Hybrid"),
    "intergrade": _("Intergrade"),
    "spuh": _("Genus"),
    "slash": _("Species group"),
    "domestic": _("Domestic"),
    "form": _("Form"),
}

EXOTIC_CODE = {
    "": "",  # NATIVE
    "N": _("Naturalized"),
    "P": _("Provisional"),
    "X": _("Escapee"),
}


class Species(models.Model):
    class Meta:
        verbose_name = _("species")
        verbose_name_plural = _("species")

    created = models.DateTimeField(
        auto_now_add=True,
        help_text=_("When was the record created."),
    )

    order = models.IntegerField(
        verbose_name=_("taxonomic order"),
        help_text=_("The position in the eBird/Clements taxonomic order."),
    )

    category = models.TextField(
        verbose_name=_("category"),
        help_text=_("The category from the eBird/Clements taxonomy."),
    )

    concept = models.TextField(
        verbose_name=_("Taxonomic Concept Identifier"),
        help_text=_("The Avibase identifier for the species."),
    )

    common_name = models.TextField(
        verbose_name=_("common name"),
        help_text=_("The species common name in the eBird/Clements taxonomy."),
    )

    scientific_name = models.TextField(
        verbose_name=_("scientific name"),
        help_text=_("The species scientific name in the eBird/Clements taxonomy."),
    )

    subspecies_common_name = models.TextField(
        blank=True,
        verbose_name=_("subspecies common name"),
        help_text=_(
            "The subspecies, group or form common name in the eBird/Clements taxonomy."
        ),
    )

    subspecies_scientific_name = models.TextField(
        blank=True,
        verbose_name=_("Scientific name"),
        help_text=_(
            "The subspecies, group or form scientific name in the eBird/Clements taxonomy."
        ),
    )

    exotic_code = models.TextField(
        blank=True,
        verbose_name=_("exotic code"),
        help_text=_("The code used if the species is non-native."),
    )

    def __repr__(self) -> str:
        return str(self.order)

    def __str__(self):
        return str(self.subspecies_common_name or self.common_name)
