from django.contrib import admin
from django.db.models import DecimalField, IntegerField, TextField
from django.forms import Textarea, TextInput
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models


class ObservationInline(admin.TabularInline):
    model = models.Observation
    fields = ("observation", "common_name", "scientific_name", "count", "comments")
    ordering = ("species__order",)
    readonly_fields = ("observation", "common_name", "scientific_name", "count", "comments")
    extra = 0

    @admin.display(description=_("Observation"))
    def observation(self, obj):
        url = reverse("admin:data_observation_change", kwargs={"object_id": obj.id})
        return format_html('<a href="{}">{}</a>', url, obj.identifier)

    @admin.display(description=_("Common name"))
    def common_name(self, obj):
        return obj.species.scientific_name

    @admin.display(description=_("Scientific name"))
    def scientific_name(self, obj):
        return format_html("<i>{}</i>", obj.species.scientific_name)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("species")
            .order_by("species__order")
        )


@admin.register(models.Checklist)
class ChecklistAdmin(admin.ModelAdmin):
    list_display = (
        "identifier",
        "date",
        "time",
        "species_count",
        "location",
        "county_code",
        "state_code",
        "country_code",
        "observer",
    )
    ordering = ("-started",)
    search_fields = ("location__name", "observer__name")
    autocomplete_fields = ("location", "observer")
    inlines = [ObservationInline]
    formfield_overrides = {
        DecimalField: {
            "widget": TextInput(),
        },
        IntegerField: {
            "widget": TextInput(),
        },
        TextField: {
            "widget": TextInput(attrs={"class": "vTextField"}),
        },
    }
    readonly_fields = ("identifier", "edited")
    fields = (
        "date",
        "time",
        "location",
        "country_code",
        "state_code",
        "county_code",
        "observer",
        "species_count",
        "complete",
        "observer_count",
        "group",
        "protocol",
        "protocol_code",
        "duration",
        "distance",
        "area",
        "comments",
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "comments":
            field.widget = Textarea(attrs={"rows": 5, "class": "vLargeTextField"})
        elif db_field.name == "data":
            field.widget = Textarea(attrs={"rows": 10, "class": "vLargeTextField"})

        return field

    def save_model(self, request, obj, form, change):
        if "location" in form.changed_data:
            location = obj.location
            obj.country = location.country
            obj.state = location.state
            obj.county = location.county
        super().save_model(request, obj, form, change)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("identifier", "name", "county", "state", "country")
    ordering = ("-identifier",)
    search_fields = ("name", "county", "state", "country")
    readonly_fields = ("identifier",)

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "name":
            field.widget = TextInput(attrs={"class": "vLargeTextField"})
        elif db_field.name == "latitude":
            field.widget = TextInput()
        elif db_field.name == "longitude":
            field.widget = TextInput()
        return field

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if "country" in form.changed_data:
            models.Checklist.objects.filter(location=obj).update(country=obj.country)
            models.Observation.objects.filter(location=obj).update(country=obj.country)
        if "state" in form.changed_data:
            models.Checklist.objects.filter(location=obj).update(state=obj.state)
            models.Observation.objects.filter(location=obj).update(state=obj.state)
        if "county" in form.changed_data:
            models.Checklist.objects.filter(location=obj).update(county=obj.county)
            models.Observation.objects.filter(location=obj).update(county=obj.county)

@admin.register(models.Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ("species", "count", "comments")
    search_fields = ("identifier", "species__common_name", "species__scientific_name")
    ordering = ("-started",)
    autocomplete_fields = ("checklist", "location", "observer", "species")
    readonly_fields = ("identifier", "edited")
    fields = (
        "species",
        "count",
        "age_sex",
        "breeding_code",
        "breeding_category",
        "behavior_code",
        "media",
        "comments",
        "checklist",
        "location",
        "country_code",
        "state_code",
        "county_code",
        "observer",
        "edited",
        "approved",
        "reviewed",
        "reason",
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "count":
            field.widget = TextInput()
        elif db_field.name == "comments":
            field.widget = Textarea(attrs={"rows": 5, "class": "vLargeTextField"})
        elif db_field.name == "data":
            field.widget = Textarea(attrs={"rows": 5, "class": "vLargeTextField"})
        return field

    def save_model(self, request, obj, form, change):
        if "location" in form.changed_data:
            location = obj.location
            obj.country = location.country
            obj.state = location.state
            obj.county = location.county

        super().save_model(request, obj, form, change)


@admin.register(models.Observer)
class ObserverAdmin(admin.ModelAdmin):
    list_display = ("identifier", "name",)
    ordering = ("identifier",)
    search_fields = ("name",)
    formfield_overrides = {
        TextField: {
            "widget": TextInput(attrs={"class": "vTextField"}),
        }
    }


@admin.register(models.Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("order", "common_name", "scientific_name", "subspecies_common_name")
    ordering = ("order",)
    search_fields = ("common_name", "scientific_name")
    formfield_overrides = {
        TextField: {
            "widget": TextInput(attrs={"class": "vTextField"}),
        }
    }
    readonly_fields = ("order",)
    fields = (
        "common_name",
        "scientific_name",
        "order",
        "concept",
        "category",
        "exotic_code",
        "subspecies_common_name",
        "subspecies_scientific_name",
    )
