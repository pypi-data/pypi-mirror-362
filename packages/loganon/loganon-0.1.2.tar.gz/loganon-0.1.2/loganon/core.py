from __future__ import annotations

from abc import ABC, abstractmethod
from collections import defaultdict
import json
import re
from typing import Any, Mapping, Sequence
from types import ModuleType
import inspect

import logging

_logger = logging.getLogger(__name__)


def get_rules(module: ModuleType) -> list[Rule]:
    """Get all the Rule subclasses from a module. Ignores abstract classes.
    
    Args:
        module: The module to get the rules from.

    Returns:
        A list of Rule subclasses.
    """
    rules = []
    for _, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and (issubclass(obj, Rule) and not inspect.isabstract(obj)):
            rules.append(obj)
    return rules

class Rule(ABC):
    """A rule defines what string patterns to look for, and how to handle them. This Rule class is
    an abstract base which defines some common logic for all rules.
    
    Do not derive from this class directly; instead, derive from one of the subclasses."""

    def __init__(self, anonymizer: Anonymizer):
        self.anonymizer = anonymizer
        """Back reference to the anonymizer which created this rule. This is used to access the
        cache, and to apply the rule to the log message."""
        self._anonymized_values = set()
    
    @property
    def cache(self) -> dict[str, str]:
        """A cache of anonymized strings. This is a dictionary which maps the original string to the
        anonymized string. The key is a string which is unique to the rule, and is used to identify
        the rule in the cache.
        
        Each rule has its own cache, but it's possible to override this behaviour by implementing
        your own cache definition in a subclass.
        """
        key = self.__module__ + "." + self.__class__.__name__
        return self.anonymizer.cache[key]
    
    @abstractmethod
    def func(self, match: re.Match) -> str:
        """Defines logic for how to anonymize a matched string. This is the main function which
        should be overridden by subclasses. The function is passed a regex Match object, which
        contains the matched string, and the groups which were matched.
        
        Args:
            match: The match object from the regex pattern.

        Returns:
            The anonymized string.
        """
        pass

    def anonymize(self, value: str) -> str:
        """Anonymize a value. This is the function called by the `replace` method. It checks if
        the value is already anonymized, and if so, returns the cached value. Otherwise, it calls
        the `func` function to anonymize the value.
        
        Args:
            value: The value to anonymize.
            
        """
        if self.is_already_anonymized(value):
            return value
        return self.func(value)

    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. This is used to avoid re-anonymizing values
        which have already been anonymized. Default behaviour involves pre-generating 50 anonymized
        values, then comparing incoming values to the set. However, any rules which use randomization
        to generate values should override this method.
        
        Args:
            value: The value to check.
        
        Returns:
            True if the value is already anonymized, False otherwise.
        """
        if not self._anonymized_values:
            # We need to use a new rule here to avoid polluting our own cache
            new_rule = self.__class__(Anonymizer({}))
            for i in range(50):
                try:
                    self._anonymized_values.add(new_rule.func(i))
                except Exception:
                    # Some rules can't genreate 50+ values (like the CountryRule)
                    break
        return value in self._anonymized_values
    
    def preprocess_match(self, match: re.Match) -> str:
        """Preprocess the match before anonymizing it. By default, we return the full match string,
        but you can use this to fetch a specific group from the match. This is useful for rules
        which use regex patterns with capture groups.

        Typically there's no need to override this method, but you can if you need advanced
        preprocessing before the `func` function is called.
        
        Args:
            match: The match object from the regex pattern.

        Returns:
            The string to replace.
        """
        return match.group(0)
    

    def _replace(self, match: re.Match) -> str:
        """To be used in re.sub as the replacement function."""
        str_to_replace = self.preprocess_match(match)
        new_str = self.anonymize(str_to_replace)
        return new_str


class TextRule(Rule, ABC):
    """Rules for text-based log messages. These rules are applied to a full log string. They
    identify regex patterns within the string and replace them with anonymized strings."""

    @property
    @abstractmethod
    def pattern(self) -> str|re.Pattern:
        """A regex pattern defining what to look for. This is a string or a compiled regex Pattern
        object."""
        pass

    @property
    def _regex_pattern(self) -> re.Pattern:
        """Return the regex pattern as a compiled regex object."""
        if not isinstance(self.pattern, re.Pattern):
            return re.compile(self.pattern)
        return self.pattern

class FieldRule(Rule, ABC):
    """Rules for field-based log messages. These rules are applied ecursively to each field in a
    log message. They're indended for use on JSON logs or other structured logs.
    
    They are defined by a field pattern, value pattern, and a function to anonymize the value. When
    evaluating a log field, the field name is checked agaist the field pattern, and the field value
    is checked against the value pattern. If both patterns match, the field is anonymized using the
    `func` function."""

    @property
    @abstractmethod
    def field_pattern(self) -> str|re.Pattern:
        """A regex pattern to match the field name. This must be specified when subclassing this
        rule."""
        pass

    @property
    def value_pattern(self) -> str|re.Pattern:
        """A regex pattern to match the field value. By default, this is set to match any value,
        but you can override this if you like."""
        return re.compile(".*")

class _EasyRuleMixin:
    """Interface which automates checking the cache"""

    @abstractmethod
    def new_value(self) -> str:
        """Defines how to generate a new anonymized value."""
        pass

    def func(self, value: str) -> str:
        """Anonymize the matched string. Checks if the value is in the cache, and if so, returns
        the cached value. Otherwise, returns a new value."""
        if value in self.cache:
            return self.cache[value]
        new_value = self.new_value()
        self.cache[value] = new_value
        return new_value


class EasyTextRule(_EasyRuleMixin, TextRule):
    """A simple text rule that can be used to anonymize text. Automatically checks the cahe for a
    replacement value and only generates a new value if it's not in the cache."""

    @abstractmethod
    def new_value(self) -> str:
        """Defines how to generate a new anonymized value. This is called when the value is not in
        the cache, and must be overridden by subclasses."""
        pass

class EasyFieldRule(_EasyRuleMixin, FieldRule):
    """A simple field rule that can be used to anonymize fields. Automatically checks the cahe for a
    replacement value and only generates a new value if it's not in the cache."""

    @abstractmethod
    def new_value(self) -> str:
        """Defines how to generate a new anonymized value. This is called when the value is not in
        the cache, and must be overridden by subclasses."""
        pass
    
class Anonymizer:
    """Anonymizes log messages based on a set of rules. The Anonymizer class contains the cache
    all rules use to anonymize log messages, and also contrains the logic used to extract sensitive
    information and replace it with anonymized values as defined by the rules."""

    def __init__(self, rules: list[Rule | ModuleType]):
        """Initialize the anonymizer with a list of rules.
        
        Args:
            rules (list[Rule|ModuleTyle]): A list of rules to apply to the log messages. The order of the
            rules determines the priority of the rules.
        """
        self.cache: dict[str, str] = defaultdict(dict)
        """The cache is used to keep track of values previously anonymized by a rule and ensure
        they are replaced with the same value if they're encountered again."""
        self.rules: list[Rule|ModuleType] = []
        """The rules to apply to the log messages. This is a list of Rule objects, or modules
        containing Rule subclasses. If an item is a module, it is scanned, and any classes defined
        within which inherit from Rule are added to the rules list. (This excludes any such classes
        which are abstract, allowing you to define a custom asbtarct rule class to inherit your
        custom rules from.)"""
        for item in rules:
            if inspect.ismodule(item):
                self.rules.extend(get_rules(item))
            elif issubclass(item, Rule):
                self.rules.append(item(self))
            else:
                raise ValueError(f"Invalid rule type: {type(item)} - {item}")
    
    def anonymize(self, log_message: str) -> str:
        """Takes a log message as a string and applies all `TextRules`'s to the string. Afterword,
        attempts to parse the log as a JSON string; if successful, it will then apply any
        `FieldRule`s to the deserialized log, and replace any values in the log with cached values
        `TextRule`s, if they were encountered in the original pass.
        
        Args:
            log_message (str): The log message to anonymize.
            
        Returns:
            str: The anonymized log message, re-serialized as a string, if it was deserialized.
        """
        # TODO: Support other formats, such as XML, YAML, etc.
        log_message = self.anonymize_string(log_message)
        try:
            log = json.loads(log_message)
            return json.dumps(self.anonymize_dict(log))
        except json.JSONDecodeError:
            return log_message
        
    def anonymize_string(self, log_message: str) -> str:
        """Anonymize a log message based on the rules. Applied all `TextRule`s to the message.
        
        Args:
            log_message (str): The log message to anonymize.
            
        Returns:
            str: The anonymized log message.
        """
        # Collect all matches from all rules
        matches = []
        for rule in self.rules:
            if isinstance(rule, FieldRule):
                continue # Skip rules for field-based anonymization
            for match in rule._regex_pattern.finditer(log_message):
                span = match.span()
                if groups := match.groups():
                    for idx, group in enumerate(groups):
                        if group:
                            span = match.span(idx + 1)
                            break
                matches.append({
                    'start': span[0],
                    'end': span[1],
                    'range': set(range(span[0], span[1])),
                    'match': match,
                    'func': rule._replace,
                    'pattern': rule.pattern,
                    'preprocess_match': rule.preprocess_match
                })

        # Filter out overlapping matches
        non_overlapping = []
        for match in matches:
            if not any(m['range'] & match['range'] for m in non_overlapping):
                non_overlapping.append(match)

        # Apply the anonymization functions to the non-overlapping matches
        for match in sorted(non_overlapping, key=lambda x: x['start'], reverse=True):
            new_value = match['func'](match['match'])
            _logger.debug(f"Replacing {log_message[match['start']:match['end']]} with {new_value}")
            log_message = log_message[:match['start']] + new_value + log_message[match['end']:]
        
        return log_message
    
    def anonymize_dict(self, log: Mapping[str, Any], replace_from_text_cache: bool = True) -> str:
        """Anonymize a dictionary. Applied all `FieldRule`s to the dictionary. Additionally, can
        also check if the value of each field is in the cache of a `TextRule` and replace it.
        
        Args:
            log (Mapping[str, Any]): The log to anonymize.
            replace_from_text_cache (bool): Whether to replace values in the log with values from
            the cache of a `TextRule` if they are present. Defaults to `True`.
            
        Returns:
            Mapping[str, Any]: The anonymized log.
        """
        def anonymize_value(key: str, value: Any) -> str:
            original_type = str
            if isinstance(value, int) or isinstance(value, float):
                original_type = type(value)
                value = str(value)
            if isinstance(value, str):
                for rule in self.rules:
                    if isinstance(rule, FieldRule):
                        if rule.field_pattern.fullmatch(key) and rule.value_pattern.fullmatch(value):
                            new_value = rule.func(value)
                            _logger.debug(f"Replacing {value} with {rule.func(value)}")
                            return original_type(new_value)
                    else:
                        if replace_from_text_cache and value in rule.cache:
                            _logger.debug(f"{rule.__class__.__name__}: Replacing {value} with {rule.cache[value]} from cache")
                            return original_type(rule.cache[value])
            elif isinstance(value, Mapping):
                return {k: anonymize_value(k, v) for k, v in value.items()}
            elif isinstance(value, Sequence):
                return [anonymize_value(key, v) for v in value]
            return original_type(value)
        
        return {k: anonymize_value(k, v) for k, v in log.items()}
    
