import csv
import datetime as dt
import logging
import re
from decimal import Decimal
from pathlib import Path

from django.utils.timezone import get_default_timezone

from .models import Checklist, Location, Observation, Observer, Species

logger = logging.getLogger(__name__)


class BasicDatasetLoader:
    @staticmethod
    def add_location(data: dict[str, str]) -> Location:
        identifier: str = data["LOCALITY ID"]
        location: Location

        values: dict = {
            "identifier": identifier,
            "type": data["LOCALITY TYPE"],
            "name": data["LOCALITY"],
            "county": data["COUNTY"],
            "county_code": data["COUNTY CODE"],
            "state": data["STATE"],
            "state_code": data["STATE CODE"],
            "country": data["COUNTRY"],
            "country_code": data["COUNTRY CODE"],
            "latitude": Decimal(data["LATITUDE"]),
            "longitude": Decimal(data["LONGITUDE"]),
            "iba_code": data["IBA CODE"],
            "bcr_code": data["BCR CODE"],
            "usfws_code": data["USFWS CODE"],
            "atlas_block": data["ATLAS BLOCK"],
            "url": "https://ebird.org/region/%s" % identifier,
        }

        if location := Location.objects.filter(identifier=identifier).first():
            for key, value in values.items():
                setattr(location, key, value)
            location.save()
        else:
            location = Location.objects.create(**values)
        return location

    @staticmethod
    def add_observer(data: dict[str, str]) -> Observer:
        identifier: str = data["OBSERVER ID"]
        observer: Observer

        values: dict = {
            "identifier": identifier,
            "name": "",
        }

        if observer := Observer.objects.filter(identifier=identifier).first():
            for key, value in values.items():
                setattr(observer, key, value)
            observer.save()
        else:
            observer = Observer.objects.create(**values)
        return observer

    @staticmethod
    def add_species(data: dict[str, str]) -> Species:
        order = data["TAXONOMIC ORDER"]
        species: Species

        values: dict = {
            "order": order,
            "concept": data["TAXON CONCEPT ID"],
            "category": data["CATEGORY"],
            "common_name": data["COMMON NAME"],
            "scientific_name": data["SCIENTIFIC NAME"],
            "subspecies_common_name": data["SUBSPECIES COMMON NAME"],
            "subspecies_scientific_name": data["SUBSPECIES SCIENTIFIC NAME"],
            "exotic_code": data["EXOTIC CODE"],
        }

        if species := Species.objects.filter(order=order).first():
            for key, value in values.items():
                setattr(species, key, value)
            species.save()
        else:
            species = Species.objects.create(**values)
        return species

    @staticmethod
    def add_observation(
        data: dict[str, str], checklist: Checklist, species: Species
    ) -> Observation:
        identifier = data["GLOBAL UNIQUE IDENTIFIER"].split(":")[-1]
        observation: Observation

        values: dict = {
            "edited": checklist.edited,
            "identifier": identifier,
            "checklist": checklist,
            "location": checklist.location,
            "county_code": checklist.location.county_code,
            "state_code": checklist.location.state_code,
            "country_code": checklist.location.country_code,
            "observer": checklist.observer,
            "species": species,
            "date": checklist.date,
            "time": checklist.time,
            "started": checklist.started,
            "count": 0,
            "breeding_code": data["BREEDING CODE"],
            "breeding_category": data["BREEDING CATEGORY"],
            "behavior_code": data["BEHAVIOR CODE"],
            "age_sex": data["AGE/SEX"],
            "media": bool(data["HAS MEDIA"]),
            "approved": bool(data["APPROVED"]),
            "reviewed": bool(data["REVIEWED"]),
            "reason": data["REASON"] or "",
            "comments": data["SPECIES COMMENTS"] or "",
            "urn": data["GLOBAL UNIQUE IDENTIFIER"],
        }

        if re.match(r"\d+", data["OBSERVATION COUNT"]):
            values["count"] = int(data["OBSERVATION COUNT"])

        if observation := Observation.objects.filter(identifier=identifier).first():
            for key, value in values.items():
                setattr(observation, key, value)
            observation.save()
        else:
            observation = Observation.objects.create(**values)

        return observation

    @staticmethod
    def add_checklist(
        row: dict[str, str],
        location: Location,
        observer: Observer,
    ) -> Checklist:
        identifier: str = row["SAMPLING EVENT IDENTIFIER"]
        checklist: Checklist

        values: dict = {
            "identifier": identifier,
            "edited": dt.datetime.fromisoformat(row["LAST EDITED DATE"]).replace(
                tzinfo=get_default_timezone()
            ),
            "location": location,
            "county_code": location.county_code,
            "state_code": location.state_code,
            "country_code": location.country_code,
            "observer": observer,
            "group": row["GROUP IDENTIFIER"],
            "observer_count": row["NUMBER OBSERVERS"],
            "date": dt.datetime.strptime(row["OBSERVATION DATE"], "%Y-%m-%d").date(),
            "time": None,
            "protocol": row["PROTOCOL TYPE"],
            "protocol_code": row["PROTOCOL CODE"],
            "project_code": row["PROJECT CODE"],
            "duration": None,
            "distance": None,
            "area": None,
            "complete": bool(row["ALL SPECIES REPORTED"]),
            "comments": row["TRIP COMMENTS"] or "",
            "url": "https://ebird.org/checklist/%s" % identifier,
        }

        if time := row["TIME OBSERVATIONS STARTED"]:
            values["time"] = dt.datetime.strptime(time, "%H:%M:%S").time()
        else:
            values["time"] = dt.time(hour=0, minute=0, second=0, microsecond=0)

        values["started"] = dt.datetime.combine(
            values["date"], values["time"], tzinfo=get_default_timezone()
        )

        if duration := row["DURATION MINUTES"]:
            values["duration"] = Decimal(duration)

        if distance := row["EFFORT DISTANCE KM"]:
            values["distance"] = Decimal(distance)

        if area := row["EFFORT AREA HA"]:
            values["area"] = Decimal(area)

        if checklist := Checklist.objects.filter(identifier=identifier).first():
            for key, value in values.items():
                setattr(checklist, key, value)
            checklist.save()
        else:
            checklist = Checklist.objects.create(**values)

        return checklist

    def load(self, path: Path) -> None:
        if not path.exists():
            raise IOError('File "%s" does not exist' % path)

        loaded: int = 0

        logger.info("Loading eBird Basic Dataset", extra={"path": path})

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile, delimiter="\t")
            for row in reader:
                location: Location = self.add_location(row)
                observer: Observer = self.add_observer(row)
                checklist: Checklist = self.add_checklist(row, location, observer)
                species: Species = self.add_species(row)
                self.add_observation(row, checklist, species)

                loaded += 1

        logger.info(
            "Loaded eBird Basic Dataset",
            extra={
                "path": path,
                "loaded": loaded,
            },
        )
