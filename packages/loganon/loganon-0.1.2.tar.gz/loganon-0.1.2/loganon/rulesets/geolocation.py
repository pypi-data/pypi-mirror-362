"""Rules for anonymizing geolocation data."""

import random
import re
import string
from loganon.core import EasyFieldRule
from loganon.util import next_numeric_id

# Sample city names to return pseudorandomly
# One day I'd like to actually use these full values, but for now we'll just use the city name
_cities = [
    "Amnesty Bay",
    "Blue Valley",
    "Central City",
    "Elmond",
    "Fawcett City",
    "Gotham",
    "Ivytown",
    "Metropolis",
    "National City",
    "Smallville",
    "Star City",
    "Flavortown"
]

_shuffled_cities = _cities.copy()
random.shuffle(_shuffled_cities)

# Sample state names to return pseudorandomly
_states = [
    "East Wyomington",
    "New Texonia",
    "Missibama",
    "Calizona",
    "Arkobraska",
    "New Toba",
    "Pennibraska",
    "Ohiowa",
    "Georgibama",
    "Illibama",
    "Nevibama",
    "Alabraska",
    "Albertio",
    "Saskerta",
    "Quebedor",
    "Brunsia",
    "Nevario Island",
    "Mainche",
    "Massigan"
]
_shuffled_states = _states.copy()
random.shuffle(_shuffled_states)

# Sample country names to return pseudorandomly
_countries = [
    "Homelandia",
    "Pretenia",
    "Narnia",
    "Wakanda",
    "Rohan",
    "Mordor",
    "Gondor",
    "Freedonia",
    "Themyscira"
]

_shuffled_countries = _countries.copy()
random.shuffle(_shuffled_countries)

def make_fake_city() -> str:
    """Generates a fake city name."""

    city_name_prefixes = [
        "Hacker",
        "Virus",
        "Security",
        "Cloud",
        "Cyber",
        "Tech",
    ]
    city_name_suffixes = [
        "ville",
        "burg",
        "ton",
        "by",
        "ham",
        "bury",
        "field",
        " City",
        " Town",
        " Valley",
    ]
    return random.choice(city_name_prefixes) + random.choice(city_name_suffixes)


class CityRule(EasyFieldRule):
    """Looks for fields which indicate a city name and anonymizes the value.
    
    - Field Pattern: ``.*?city``
    - Value Pattern: ``(?:[A-Z]{2}|(?:[A-Z][a-z\s][A-Za-z\s]*))``
    """
    field_pattern = re.compile(r".*?city", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"(?:[A-Z]{2}|(?:[A-Z][a-z\s][A-Za-z\s]*))")
    """@private"""

    def new_value(self) -> str:
        cached_cities = set(self.cache.values())
        if len(cached_cities) < len(_shuffled_cities):
            return _shuffled_cities[len(cached_cities)]
        return make_fake_city()

class StateRule(EasyFieldRule):
    """Looks for fields which indicate a state name and anonymizes the value.
    
    - Field Pattern: `.*?state`
    - Value Pattern: `[A-Z][A-Za-z\s]+`
    """
    field_pattern = re.compile(r"state", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[A-Z][A-Za-z\s]+") # Lke California, but not CLOSED or closed
    """@private"""

    def new_value(self) -> str:
        """@private"""
        cached_states = set(self.cache.values())
        if len(cached_states) < len(_shuffled_states):
            return _shuffled_states[len(cached_states)]
        # generate a random name by portmanteauing two random statses
        state1, state2 = random.sample(_shuffled_states, 2)[:2]
        return state1[:(len(state1)//2)] + state2[(len(state2)//2):]


class StateAbbreviationRule(EasyFieldRule):
    """Looks for fields which indicate a state abbreviation and anonymizes the value.
    
    - Field Pattern: `.*?state`
    - Value Pattern: `[A-Z]{2}`
    """
    field_pattern = re.compile(r"state", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[A-Z]{2}")
    """@private"""

    def new_value(self) -> str:
        """@private"""
        return "X" + random.choice(string.ascii_uppercase)
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value.startswith("X")


class CountryRule(EasyFieldRule):
    """Looks for fields which indicate a country name and anonymizes the value.
    
    - Field Pattern: `.*?country`
    - Value Pattern: `[A-Z][A-Za-z\s]+`
    """
    field_pattern = re.compile(r"country", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[A-Z][A-Za-z\s]+")
    """@private"""

    def new_value(self) -> str:
        """@private"""
        return _shuffled_countries[len(self.cache)]

class PostalCodeRule(EasyFieldRule):
    """Looks for fields which indicate a postal code and anonymizes the value.
    
    - Field Pattern: `post(?:al)?[_\-\s]?(?:code)?`
    - Value Pattern: `[A-Z\d\s-]{2,}`
    """
    field_pattern = re.compile(r"post(?:al)?[_\-\s]?(?:code)?", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[A-Z\d\s-]{2,}")
    """@private"""

    def new_value(self) -> str:
        """@private"""
        return next_numeric_id(5, self.cache)


class LatitudeRule(EasyFieldRule):
    """Looks for fields which indicate a latitude and anonymizes the value.
    
    - Field Pattern: `lat(?:itude)?`
    - Value Pattern: `[\+\-]?\d+(?:\.\d+)?`
    """
    field_pattern = re.compile(r"lat(?:itude)?", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[\+\-]?\d+(?:\.\d+)?")
    """@private"""

    def new_value(self) -> str:
        """@private"""
        return f"{random.randint(-9, 9)}0"

class LongitudeRule(EasyFieldRule):
    """Looks for fields which indicate a longitude and anonymizes the value.
    
    - Field Pattern: `lon(?:g(?:itude)?)?`
    - Value Pattern: `[\+\-]?\d+(?:\.\d+)?`
    """

    field_pattern = re.compile(r"lon(?:g(?:itude)?)?", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[\+\-]?\d+(?:\.\d+)?")
    """@private"""

    def new_value(self) -> str:
        """@private"""
        return f"{random.randint(-18, 18)}0"
