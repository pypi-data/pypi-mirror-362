"""Defines profiles for users."""

from dataclasses import dataclass
import faker
from rapidfuzz import fuzz

fake = faker.Faker()

@dataclass
class _Profile:
    first_name: str
    last_name: str
    email: str
    username: str

default_profiles = [
    _Profile("Lex", "Luthor", "lex@lexcorp.com", "lexluthor"),
    _Profile("Mercy", "Graves", "mercy@lexcorp.com", "mercy"),
    _Profile("Eve", "Tessmacher", "eve@lexcorp.com", "eve"),
    _Profile("Bruce", "Wayne", "bruce@justice.org", "batman"),
    _Profile("Clark", "Kent", "clark@justice.org", "superman"),
    _Profile("Diana", "Prince", "diana@justice.org", "wonderwoman"),
    _Profile("Barry", "Allen", "barry@justice.org", "flash"),
    _Profile("Hal", "Jordan", "hal@justice.org", "greenlantern"),
    _Profile("Arthur", "Curry", "arthur@justice.org", "martianmanhunter"),
    _Profile("Oliver", "Queen", "oliver@justice.org", "arrow"),
    _Profile("John", "Stewart", "john@justice.org", "johnstewart"),
    _Profile("Aragorn", "Elessar", "aragorn@lotr.com", "strider"),
    _Profile("Frodo", "Baggins", "frodo@lotr.com", "frodo"),
    _Profile("Samwise", "Gamgee", "sam@lotr.com", "sam"),
    _Profile("Meriadoc", "Brandybuck", "meriadoc@lotr.com", "meriadoc"),
    _Profile("Peregrin", "Took", "peregrin@lotr.com", "peregrin"),
    _Profile("Boromir", "Son of Denethor", "boromir@lotr.com", "boromir"),
    _Profile("Gimli", "Son of Gloin", "gimli@lotr.com", "gimli"),
    _Profile("Legolas", "Son of Thranduil", "legolas@lotr.com", "legolas"),
    _Profile("Gandalf", "the Grey", "gandalf@lotr.com", "gandalf"),
    _Profile("Saruman", "the White", "saruman@lotr.com", "saruman"),
    _Profile("Sauron", "the Dark Lord", "sauron@lotr.com", "sauron"),
    _Profile("Elrond", "Half-Elven", "elrond@lotr.com", "elrond"),
    _Profile("Galadriel", "Elven Lady", "galadriel@lotr.com", "galadriel"),
    _Profile("Eowyn", "Daughter of Eomer", "eowyn@lotr.com", "eowyn"),
    _Profile("Faramir", "Son of Denethor", "faramir@lotr.com", "faramir"),
    _Profile("Denethor", "Lord of Minas Tirith", "denethor@lotr.com", "denethor"),
]

def get_profiles(domain: str = None) -> list[_Profile]:
    """Get a list of profiles for a given domain.
    
    Args:
        domain: an optional domain for the user's email, if required. If not specified, a random one is chosen.
    """
    if domain:
        return [p for p in default_profiles if p.email.split("@")[-1] == domain]
    else:
        return default_profiles

def new_profile(domain: str = None) -> _Profile:
    """If, for some reason, the default profiles aren't sufficient, we can generate a new random
    one.
    
    Args:
        domain: an optional domain for the user's email, if required. If not specified, a random one is chosen.
    """

    # Faker provides a random profile generator, but it provides completely random values, so the
    #   username/name/email would all be different.
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = first_name.lower()[0] + last_name.lower()
    email = username + "@" + domain if domain else username + "@" + fake.domain_name()
    return _Profile(
        first_name,
        last_name,
        email,
        username
    )

def _compare_names(name1: str, name2: str) -> bool:
    """Compare two names to see if they are the same.
    
    Args:
        name1: the first name to compare.
        name2: the second name to compare.
    """
    if name1.casefold() == name2.casefold():
        return True
    
    fuzzy_match_scores = [
        fuzz.ratio(name1, name2),
        fuzz.partial_ratio(name1, name2),
        fuzz.token_sort_ratio(name1, name2),
        fuzz.token_set_ratio(name1, name2)
    ]

    if max(fuzzy_match_scores) > 50:
        return True
    
    return False

class UsernameDict(dict[str, _Profile]):
    """A dictionary of usernames to profiles."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = 0
    
    def __getitem__(self, key: str) -> _Profile:
        """Get a profile by username.
        
        Args:
            key: the username to get the profile for.
        """
        if super().__contains__(key):
            return super().__getitem__(key)
        
        for existing_key in self.keys():
            if _compare_names(key, existing_key):
                return super().__getitem__(existing_key)

        return super().__getitem__(key)
    
    def get(self, key: str, default: _Profile = None) -> _Profile:
        """Get a profile by username.
        
        Args:
            key: the username to get the profile for.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def __setitem__(self, key: str, value: _Profile):
        """Set a profile by username.
        
        Args:
            key: the username to set the profile for.
        """
        
        found_existing_key = False
        for existing_key in self.keys():
            if _compare_names(key, existing_key):
                found_existing_key = True
                super().__setitem__(existing_key, value)
        
        if not found_existing_key:
            self._length += 1 # Only increase length for new items
        
        return super().__setitem__(key, value)

    def __len__(self) -> int:
        """Get the length of the dictionary."""
        return self._length
    
    def __contains__(self, key: str) -> bool:
        """Check if a username is in the dictionary."""
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False
        
        