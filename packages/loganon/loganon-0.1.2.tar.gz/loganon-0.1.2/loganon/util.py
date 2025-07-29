"""The utility module contains functions that are used throughout the library. They are mainly
helper functions which allow you to easily generate a random value without thinking too much about
it."""

import random
import string
from typing import Any, Iterable

from rapidfuzz import fuzz


def random_string(length: int) -> str:
    """Generates a random string of a given length.

    Args:
        length (int): The length of the string to generate.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def random_id(prefix: str, length: int) -> str:
    """Generates a random ID with a given prefix and length. The total length of the ID will be the
    length of the prefix plus the length of the random string.
    
    Args:
        prefix (str): The prefix to add to the ID.
        length (int): The length of the random string to generate.
    """
    return f"{prefix}{random_string(length)}"

def next_numeric_id(length: int, iter: Iterable[Any] = []) -> str:
    """Generates a random numeric ID with a given prefix and length. Attempts are made to generate
    a pseudo-random ID, following the pattern `1111`, `2222`, `3333`, etc. The position of the
    returned ID in this sequence is determined by the length of the iterable which is passed in.
    If the itterable is longer than the pseudo-random sequence, the ID will be generated using a
    random number.
    
    Args:
        length: The length of the ID to generate.
        iter: An existing list of IDs, the length of which will determine the ID pattern.
    """
    # It's common to need to generate a random string of numbers. Rather than have an actually
    #   random string, it looks nicer and cleaner to use a value which is clearly mocked.
    if len(iter) < 9:
        # Initially return just a string of a repeated degit
        # ex. 11111111, 22222222, 33333333, etc.
        return str(len(iter)+1) * length
    elif len(iter) < 19:
        # Use a pattern of repeating digits, which we rotate through
        # ex. 11223344, 22334455, 33445566, etc.
        s = "1234567890"
        return "".join(s[((len(iter)+i) % 10)//2] for i in range(length))
    else:
        # Fallback to actually random
        return "".join(random.choices(string.digits, k=length))
    
def next_string_id(length: int, iter: Iterable[Any] = []) -> str:
    """Generates a random string ID with a given length. Attempts are made to generate
    a pseudo-random ID, following the pattern `AAAA`, `BBBB`, `CCCC`, etc. The position of the
    returned ID in this sequence is determined by the length of the iterable which is passed in.
    If the itterable is longer than the pseudo-random sequence, the ID will be generated using a
    random string comprised of A-Z.
    
    Args:
        length: The length of the ID to generate.
        iter: An existing list of IDs, the length of which will determine the ID pattern.
    """
    if len(iter) < 6:
        # Initially return just a string of a repeated degit
        # ex. AAAAAAAA, BBBBBBBB, CCCCCCCC, etc.
        return str(len(iter)+1) * length
    elif len(iter) < 12:
        # Use a pattern of repeating digits, which we rotate through
        # ex. AABBCCDD, BBCCDDEE, CCDDEEFF, etc.
        s = "ABCDEF"
        return "".join(s[((len(iter)+i) % 6)//2] for i in range(length))
    else:
        # Fallback to actually random
        return "".join(random.choices(string.ascii_uppercase, k=length))

def next_hex_id(length: int, iter: Iterable[Any] = []) -> str:
    """Generates a random hexadecimal ID with a given length.  Attempts are made to generate
    a pseudo-random ID. The position of the returned ID in this sequence is determined by the
    length of the iterable which is passed in. If the itterable is longer than the pseudo-random
    sequence, the ID will be generated using a random hexadecimal string.
    
    Args:
        length: The length of the ID to generate.
        iter: An existing list of IDs, the length of which will determine the ID pattern.
    """
    if len(iter) < 16:
        # Use a pattern of repeating digits, which we rotate through
        # ex. AABBCCDD, BBCCDDEE, CCDDEEFF, etc.
        s = "ABCDEF1234567890"
        return "".join(s[((len(iter)+i) % 16)] for i in range(length))
    else:
        # Fallback to actually random
        return random_alphanumeric_string(length)

def random_alphanumeric_string(length: int, hex: bool = True) -> str:
    """Generates a random alphanumeric string.
    
    Args:
        length: The length of the string to generate.
        hex: Whether to use only A-F for letters, or the entire alphabet. Default is True.
    """
    if hex:
        return "".join(random.choices(string.ascii_letters[:6] + string.digits, k=length))
    else:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

def fuzzy_match(str1: str, str2: str, threshold: float = 0.6) -> bool:
    """Compare two strings to check if they are similar. Uses the `rapidfuzz` library to calculate
    the similarity score. The calculation is an average of simple ratio, partial ratio, token sort
    ratio, and token set ratio.
    
    Args:
        str1: the first string to compare.
        str2: the second string to compare.
        threshold: the threshold for the similarity score. Default is 0.6.
    
    Returns:
        `True` if the strings are similar, `False` otherwise.
    """
    if str1.casefold() == str2.casefold():
        return True
    
    fuzzy_match_scores = [
        fuzz.ratio(str1, str2),
        fuzz.partial_ratio(str1, str2),
        fuzz.token_sort_ratio(str1, str2),
        fuzz.token_set_ratio(str1, str2)
    ]

    if sum(fuzzy_match_scores)/4 > (100*threshold):
        return True
    
    return False

class FuzzyDict(dict[str, Any]):
    """A mapping of strings to values. Keys from the dictionary are fetch if they are similar-enough
    to an existing key. Mostly useful for mapping keys which are similar, but not exactly the same,
    to a single unified result.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._length = 0
    
    def __getitem__(self, key: str) -> Any:
        """Get a profile by username.
        
        Args:
            key: the username to get the profile for.
        """
        if super().__contains__(key):
            return super().__getitem__(key)
        
        for existing_key in self.keys():
            if fuzzy_match(key, existing_key):
                return super().__getitem__(existing_key)

        return super().__getitem__(key)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a profile by key. The entered key is compared to existing keys using a fuzzy match.
        Returns the first key which is similar to the entered key, or else the provided default
        value.
        
        Args:
            key: the key to get the value for.
            default: the value to return if the key is not found.

        Returns:
            The value for the key, or the default value if the key is not found.
        """
        try:
            return self.__getitem__(key)
        except KeyError:
            return default
    
    def __setitem__(self, key: str, value: Any):
        """Set a profile by username.
        
        Args:
            key: the username to set the profile for.
        """
        
        found_existing_key = False
        for existing_key in self.keys():
            if fuzzy_match(key, existing_key):
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