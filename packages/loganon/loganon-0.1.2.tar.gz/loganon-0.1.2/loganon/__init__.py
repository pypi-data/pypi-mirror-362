"""Loganon is a library for anonymizing logs. It works by defining rules for how to anonymize
different types of data, and then applying those rules to the log. The tool can be used in a python
script, or called from the command line.

The library is designed to be extensible, so you can create your own rulesets and use them to
anonymize your logs.
"""
from loganon.core import Anonymizer, get_rules, Rule, EasyTextRule, EasyFieldRule, TextRule, FieldRule
import loganon.rulesets.base
import loganon.rulesets.aws
import loganon.rulesets.geolocation

def all_rules() -> dict[str, list[Rule]]:
    """Return all the rules definined in the library. Only returns the rulesets defined in this
    package, not any custom rulesets.
    
    Args: None

    Returns:
        A dictionary with the ruleset names as keys, and a list of Rule objects as values.
    """
    return {
        "base": get_rules(loganon.rulesets.base),
        "aws": get_rules(loganon.rulesets.aws),
        "geolocation": get_rules(loganon.rulesets.geolocation),
    }

def all_rules_list() -> list[Rule]:
    """Return all the rules definined in the library. Only returns the rulesets defined in this
    package, not any custom rulesets.
    
    Args: None

    Returns:
        A list of Rule objects.
    """
    return [rule for ruleset in all_rules().values() for rule in ruleset]