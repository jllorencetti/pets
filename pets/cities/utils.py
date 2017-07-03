import csv
import itertools
import os

from django.conf import settings

from cities import models


def get_states_filename(country):
    return os.path.join(settings.CITIES_DATA_LOCATION, country.lower(), 'states.csv')


def get_cities_filename(country):
    return os.path.join(settings.CITIES_DATA_LOCATION, country.lower(), 'cities.csv')


def load_file(filename):
    with open(filename, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)


def load_states_from_file(filename):
    states = load_file(filename)

    for state in states:
        models.State.objects.get_or_create(
            code=state.get('code'),
            abbr=state.get('abbr'),
            name=state.get('name'),
        )


def load_cities_from_file(filename):
    cities = load_file(filename)
    cities = sorted(cities, key=lambda c: c['state'])
    grouped_cities = itertools.groupby(cities, key=lambda c: c['state'])

    for state_abbr, cities in grouped_cities:
        state = models.State.objects.get(abbr=state_abbr)
        for city in cities:
            models.City.objects.get_or_create(
                state=state,
                code=city.get('code'),
                name=city.get('name')
            )
