"""Some basic anomymizing rules that are useful in most cases."""

import random
import re
import string

from loganon._profiles import UsernameDict, get_profiles, new_profile
from loganon.core import Anonymizer, FieldRule, TextRule
from loganon.util import random_alphanumeric_string



class IPRule(TextRule):
    """A rule that anonymizes IP addresses. Examples of values anonymized are:
    - 192.168.2.1
    - 172.16.2.1
    - 136.81.55.112
    """
    pattern = re.compile(r"\b(?:(?:25[0-5]|(?:2[0-4]|1\d|[1-9]|)\d)\.?\b){4}\b")
    """@private"""

    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        if value == "1.2.3.4":
            return True
        if len(set(value.split("."))) == 1:
            # Check if all four components are the same
            return True
        return False

    def func(self, ip: str) -> str:
        """Anonymize an IP address. @private"""
        # List of sample anonymized IPs
        sample_ips = (
            '1.2.3.4',
            '1.1.1.1',
            '2.2.2.2',
            '3.3.3.3',
            '4.4.4.4',
            '5.5.5.5',
            '6.6.6.6',
            '7.7.7.7',
            '8.8.8.8',
            '9.9.9.9',
        )
        if ip not in self.cache:
            if len(self.cache) < len(sample_ips):
                new_ip = sample_ips[len(self.cache)]
            else:
                new_ip_in_use = True
                while new_ip_in_use:
                    new_ip = f"1.0.{random.randint(0, 255)}.{random.randint(0, 255)}"
                    new_ip_in_use = new_ip in self.cache.values()
            self.cache[ip] = new_ip
        return self.cache[ip]

class EmailRule(TextRule):
    """A rule that anonymizes email addresses. Interconnects with the UserNameRule and FullNameRule
    to attempt to keep identities consistent across the log.
    
    Examples of values anonymized are:
    - john.smith@gmail.com
    - janedoe@acme.com
    """
    
    pattern = re.compile(r"[a-zA-Z][a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
    """@private"""
    
    def __init__(self, anonymizer: Anonymizer):
        """@private"""
        super().__init__(anonymizer)
        # Create the domain cache
        key = self.__module__ + "." + "Profiles.Domains"
        self.anonymizer.cache[key] = {}
    
    @property
    def username_cache(self) -> dict[str, str]:
        """@private"""
        return self.anonymizer.cache[self.__module__ + "." + "Profiles"]
    
    @property
    def domain_cache(self) -> dict[str, str]:
        """@private"""
        return self.anonymizer.cache[self.__module__ + "." + "Profiles.Domains"]
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value in {p.email for p in get_profiles()}

    def func(self, email: str) -> str:
        """Anonymize an email address. @private"""
        # This function get's kind of ugly because emails are linked to user profiles. We have
        #   access to the user profile cache in order to check whether a this email might belong
        #   to a previously anonymized username. Additionally, if we determine that's not the case,
        #   we want to link the username inferred from this email to our newly-created anonymized
        #   profile.
        
        # Quickly, if the email is already in the cache, return it
        if email in self.cache:
            return self.cache[email]
        
        # Since the email regex isn't perfect, we might select slightly more than we should.
        #   We'll also check if any of the cached values are contained WITHIN the provided string.
        for key, val in self.cache.items():
            if key in email:
                print(key, email)
                return email.replace(key, val)

        username, domain = email.split("@")
        if domain not in self.domain_cache:
            # If the domain is not known, create a new one
            used_domains = set(self.domain_cache.values())
            profiles = get_profiles()
            anonymized_profile = None
            # Look for a pre-created profile with a new domain
            for profile in profiles:
                if profile.email.split("@")[-1] in used_domains:
                    # Skip domains in use
                    continue
                anonymized_profile = profile
            # If we exhausted the pre-set profiles, create a new one
            if not anonymized_profile:
                anonymized_profile = new_profile()
            self.domain_cache[domain] = anonymized_profile.email.split("@")[-1]
            self.username_cache[username] = anonymized_profile
            self.cache[email] = anonymized_profile.email
            return self.username_cache[username].email

        # If the domain is already known, use that
        target_domain = self.domain_cache[domain]
        for profile in get_profiles(target_domain):
            if profile.username in self.username_cache:
                continue
            self.username_cache[profile.username] = profile
            self.cache[email] = profile.email
            return profile.email
        # If we exhausted the pre-set profiles, create a new one
        anonymized_profile = new_profile(target_domain)
        self.username_cache[anonymized_profile.username] = anonymized_profile
        self.cache[email] = anonymized_profile.email
        return anonymized_profile.email

class MacAddressRule(TextRule):
    """A rule that anonymizes MAC addresses. Examples of values anonymized are:
    - 5c:1f:d1:ec:2b:ae
    - a6-e3-87-8b-f8-46
    - 9ac44f2bfb83
    """
    pattern = re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}(?:[0-9A-Fa-f]{2})\b")
    """@private"""

    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value.startswith("AA:BB:CC:DD:")

    def func(self, mac: str) -> str:
        """Anonymize a MAC address. @private"""
        # Standardize the separator for caching purposes
        standardized_mac = mac.replace(":", "-").casefold()
        sep = ":" if ":" in mac else "-"
        if cached := self.cache.get(standardized_mac):
            return cached
        new_mac = ""
        cached_values = set(self.cache.values())
        while new_mac in cached_values or not new_mac:
            # Choose a clearly mocked prefix with randomized suffix
            p1 = "".join(random.choices(string.ascii_uppercase[:6] + string.digits, k=2))
            p2 = "".join(random.choices(string.ascii_uppercase[:6] + string.digits, k=2))
            new_mac = sep.join(["AA", "BB", "CC", "DD", p1, p2])
        self.cache[standardized_mac] = new_mac
        if mac.islower():
            new_mac = new_mac.lower() # Ensure we preserve the casing of the original value
        return new_mac

class HashRule(TextRule):
    """A rule that anonymizes MD5, SHA1, and SHA256 hashes. Examples of values anonymized are:
    - 00bd4ac9b8f6511df1f3b148e988f717 (MD5)
    - 92089923ece654b2e79fd72cdb711b386661302d (SHA1)
    - 78af55e350cd06d7bfa2d82e6b135a7893e4516136fd4d4a9bfd7495596548b5 (SHA256)
    """

    pattern = re.compile(r"\b([0-9A-Fa-f]{32}|[0-9A-Fa-f]{64}|[0-9A-Fa-f]{40})\b")
    """@private"""

    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value.startswith("0"*10)

    def func(self, hash: str) -> str:
        """Anonymize a hash. @private"""
        if hash in self.cache:
            return self.cache[hash]
        new_hash = ""
        while new_hash in self.cache or not new_hash:
            new_hash = "0"*10 + random_alphanumeric_string(len(hash)-10)
        self.cache[hash] = new_hash
        return new_hash

class UserNameRule(FieldRule):
    """A rule that anonymizes user names. Interconnects with the EmailRule and FullNameRule to
    attempt to keep identities consistent across the log. Only matches fields with titles looking
    like "user name" and with values that contains no special characters.
    
    Examples of fields:
        - username
        - all_user_names
    """
    field_pattern = re.compile(r".*?user[_\.\-\s]?names?", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[\w\.-]+")
    """@private"""

    def __init__(self, anonymizer: Anonymizer):
        """@private"""
        super().__init__(anonymizer)
        key = self.__module__ + "." + "Profiles"
        self.anonymizer.cache[key] = UsernameDict()
    
    @property
    def cache(self) -> UsernameDict:
        """@private"""
        return self.anonymizer.cache[self.__module__ + "." + "Profiles"]
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value in {p.username for p in get_profiles()}

    def func(self, value: str) -> str:
        """Anonymize a user name. @private"""
        normalized = self.normalize_username(value)
        if p := self.cache.get(normalized):
            return p.username
        # Get the next random profile
        profiles = get_profiles()
        anonymous_profile = None
        for profile in profiles:
            if profile not in self.cache.values():
                anonymous_profile = profile
        if not anonymous_profile:
            anonymous_profile = new_profile()
        self.cache[normalized] = anonymous_profile
        return anonymous_profile.username
    
    def normalize_username(self, username: str) -> str:
        """Normalize a username to a standard format. @private"""
        return "".join(x if x.isalpha() else " " for x in username.lower())

class FullNameRule(FieldRule):
    """A rule that anonymizes full names. Interconnects with the UserNameRule to attempt to keep
    identities consistent across the log. Only matches fields with titles ending in "name" and
    which have values that contain only letters and spaces.
    
    Examples of fields:
        - name
        - full_name
        - first_name
    """

    field_pattern = re.compile(r".*?(:?full|first).*?name|name", flags=re.IGNORECASE)
    """@private"""
    value_pattern = re.compile(r"[A-Za-z\s]+")
    """@private"""

    @property
    def cache(self) -> UsernameDict:
        """Use the same cache as the username rule. @private"""
        return self.anonymizer.cache[self.__module__ + "." + "Profiles"]

    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        return value in {p.first_name + " " + p.last_name for p in get_profiles()}

    def func(self, value: str) -> str:
        """Anonymize a full name. @private"""
        # Find a matching profile, if it exists
        normalized_name = value.lower()
        if profile := self.cache.get(normalized_name):
            return profile.first_name + " " + profile.last_name

        # If no profile is found, create a new one
        profiles = get_profiles()
        anonymous_profile = None
        for profile in profiles:
            if profile not in self.cache.values():
                anonymous_profile = profile
        if not anonymous_profile:
            anonymous_profile = new_profile()
        
        self.cache[normalized_name] = anonymous_profile
        return anonymous_profile.first_name + " " + anonymous_profile.last_name