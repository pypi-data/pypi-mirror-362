# Loganon

Loganon is a log anonymization (sometimes called 'log stripping' or 'log masking') tool designed to automatically remove PII and other sensitive information from logs. It works by applying a set of rules to a body of text which identify specific patterns and replace them with clearly fake data. The intention is to keep the underlying structure of the data as similar as possible while removing any identifying details for privacy and security.

## Usage

### CLI

Installing `loganon` via `pip` also includes a command-line interface. You can invoke it to anonymize a file according to a specific rule-set:

```bash
loganon run <RULESETS> -i <INPUT FILE> -o <OUTPUT FILE> 
```

For example, to run the core and AWS rules on a log file `cloudtrail.json`, you could run:

```bash
loganon run aws base -i cloudtrail.json -o anonymized_cloudtrail.json`
```

### As a Python Module

You can create your own Anonymizer object in a Python script. For example, to create an Anonymizer with all default rules:

```python
from loganon import Anonymizer, all_rules_list

anonymizer = Anonymizer(all_rules_list())
```

You could then anonymize any arbitrary string or dictionary by calling either the `anonymize`, `anonymize_string`, or `anonymize_dict` functions.

## Custom Rules and Rulesets

You can add custom rules by defining a Python module and registering it with the `loganon` tool. Below is a quick example of a simple custom rule module:

```python
import random, re
from loganon import EasyTextRule

class MyCustomRule(EasyTextRule):
    """Detect phone numbers and redact them."""

    pattern = re.compile(r"\b\d\d\d-\d\d\d\d\b") # Regex pattern to identify phone number, i.e. 123-4567

    def new_value(self):
        # This is how you define a new value to be returned
        # In this case, we want to return a number which starts with 555 (so you know it's fake),
        # and then has a random suffix.
        return f"555-{random.randint(0,9999):0:4}"
```

You can then register the rule permanently on the CLI with

```bash
loganon config -r custom_rules /path/to/my/python/file.py
```

Or, if using the tool as a Python module, simply pass along the custom module when you construct the anonymizer.

```python
from loganon import Anonymizer
import my_custom_rules

anon = Anonymizer([my_custom_rules])
```

### Rule Types

`loganon` has 2 basic rule types you can use: `TextRule` and `FieldRule`. Each of these has a simple version which includes some additional common logic which you can use for most cases: `EasyTextRule` and `EasyFieldRule`. Each type is detailed below.

#### EasyTextRule

To create an `EasyTextRule`, you need to provide a regex pattern to help identify what text to look for, and a function which defines how to generate new anonymized values. You don't need to worry about value caching in this class; that's all handled automatically.

Example:

```python
class MyCustomRule(EasyTextRule):
    """Detect phone numbers and redact them."""

    pattern = re.compile(r"\b\d\d\d-\d\d\d\d\b") # Regex pattern to identify phone number, i.e. 123-4567

    def new_value(self):
        # This is how you define a new value to be returned
        # In this case, we want to return a number which starts with 555 (so you know it's fake),
        # and then has a random suffix.
        return f"555-{random.randint(0,9999):0:4}"
```

#### EasyFieldRule

To create an `EasyFieldRule`, there are two patterns you can specify: one for the field name, and one for the value. The value pattern is optional; if left undefined, the rule will only check whether the field pattern is satisfied.

Example:

```python
class MyCustomRule(EasyFieldRule):
    """Detect phone numbers and redact them."""

    field_pattern = re.compile(r".*(?:phone|cell).*")
    value_pattern = re.compile(r"\b\d\d\d-\d\d\d\d\b") # Regex pattern to identify phone number, i.e. 123-4567

    def new_value(self):
        # This is how you define a new value to be returned
        # In this case, we want to return a number which starts with 555 (so you know it's fake),
        # and then has a random suffix.
        return f"555-{random.randint(0,9999):0:4}"
```

#### TextRule

The more complex text rule allows you to do more advanced features, like manipulate the cache lookup, use the original value to inform your new value, etc. Let's consider a case like an AWS ARN; we want to add additional text to our pattern to prevent overmatching, but we don't want to replace all that additional text. For this we can use groups!

```python
from loganon import TextRule
from loganon.util import random_id

class MyCustomRule(TextRule):
    pattern = re.compile(r"arn:aws:iam::\d{12}:role\/(.*?)\b")
    # This pattern needs the additional context to know it's an ARN; if we made a pattern for just `.*?`,
    # we match everything! Adding this prefix allows us to ensure we only mask the sensitive info.

    def func(self, value: str):
        """func defines how to replace the value. We receive the original, unaltered value as input."""

        # Notably, we don't automate cache lookup for TextRule, so we have to handle that manually.
        if value in self.cache:
            return self.cache[value]
        
        # Now we can create a new anonymous value
        # This will return something like "SampleRole-x8Y6q7"
        return random_id(prefix="SampleRole-", length=6)
```

#### FieldRule

Like `TextRule`, `FieldRule` lets you perform more complex analysis. Once again, the value pattern is optional, but the field pattern is required.

```python
class MyCustomRule(FieldRule):
    """Sample custom rule which just anonymizes the 24-bit subnet and leaves the last part of an IP address the same."""

    field_pattern = re.compile(".*[_\s-\b]ip[_\s-\b].*", flags=re.IGNORECASE)
    value_pattern = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

    def func(self, value: str):
        if value in self.cache:
            return self.cache[value]
        
        last_part = value.split(".")[-1]
        new_subnet = ".".join([random.randint(0,9),]*3)
        return f"{new_subnet}.{last_part}"
```

### Common Patterns

#### Multi-value anonymizing

Sometimes you want to mask multiple values inside a single pattern. While you can't write one rule that anonymizes two things, you can write two rules using the same pattern.

To do so, create a pattern that has two (or more) [capture groups](https://regexone.com/lesson/capturing_groups). Use this pattern for two rules, but override the `preprocess_match` function for each rule to ensure it operates on the correct group. Here's an example using AWS ARNs.

```python
pattern = re.compile(r"arn:aws::iam:(\d{12}):role\/(.*?)")

class AccountIdRule(EasyTextRule):
    def preprocess_match(self, match: re.Match) -> str:
        return match.group(1)
    
    def new_value(self):
        return next_numeric_id(12, iter=self.cache)
    
class RoleNameRule(EasyTextRule):
    def preprocess_match(self, match: re.Match) -> str:
        return match.group(2)
    
    def new_value(self):
        return random_id(prefix="SampleRole-", length=6)

```

#### Sharing Caches Between Rules

Sometimes you have fields which are tightly intertwined, like usernames and emails, and it's useful to be able to update both caches from within the same rule. This is supported by accessing the `Anonymizer` object's own cache instance directly.

Each rule, when instantiated, contains a backreference to the Anonymizer as `self.anonymizer`, so you can reference any arbitrary cache from inside a rule function as such:

```python
other_cache = self.anonymizer.cache["key for other cache"]
```

This requires you to know the cache key for the other rule. By default, the cache key is determined by the following pattern: `<MODULE_NAME>.<CLASS_NAME>`. However, you can override this for a custom rule by defining your own `cache` property:

```python
class MyRule(SomeRule):
    @property
    def cache(self):
        key = "A customized cache key"
        return self.anonymizer.cache[key]
```

Note that the key should be as unique as possible, to avoid collisions with other rules using the cache. Avoid short names like "emails".
