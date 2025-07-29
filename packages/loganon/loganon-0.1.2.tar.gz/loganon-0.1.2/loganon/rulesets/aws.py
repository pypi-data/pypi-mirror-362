from abc import ABC, abstractmethod
import re
from typing import Any, Callable, Iterable

from names_generator import generate_name

from loganon.core import TextRule
from loganon.util import next_numeric_id, next_hex_id


class BaseIdRule(TextRule, ABC):
    """Several types of AWS IDs are just a common prefix with random alphanumeric strings 
    following. We can consolidate some of the logic into this base class. @private"""

    # Function to choose which ID generator to use
    generator: Callable[[int, Iterable[Any]], str] = next_hex_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generator = lambda *a, **k: type(self).generator(*a, **k)
        self.anonymized_ids = set()

    @property
    @abstractmethod
    def prefix(self) -> str:
        """@private"""
        pass

    @property
    def length(self) -> int:
        return 1

    def func(self, id: str) -> str:
        new_id = ""
        if id not in self.cache:
            cached_ids = set(self.cache.values())
            while not new_id or new_id in cached_ids:
                new_id = f"{self.prefix}{self.generator(self.length, cached_ids)}"
            self.cache[id] = new_id
        return self.cache[id]
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        if not self.anonymized_ids:
            for _ in range(50):
                self.anonymized_ids.add(f"{self.prefix}{self.generator(self.length, self.anonymized_ids)}")
        return value in self.anonymized_ids


class AccountIdRule(BaseIdRule):
    """A rule that anonymizes AWS account IDs."""
    pattern = re.compile(r"\b(\d{12})\b")
    """@private"""
    prefix = ""
    """@private"""
    length = 12
    """@private"""
    generator = next_numeric_id
    """@private"""
    


class PrincipalIdRule(BaseIdRule):
    """A rule that anonymizes AWS principal IDs."""
    pattern = re.compile(r"AROA[A-Z\d]{17}")
    """@private"""
    prefix = "AROA-MOCKPRINCIPALID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""


class SessionIssuerIdRule(BaseIdRule):
    """A rule that anonymizes AWS session issuer IDs."""
    pattern = re.compile(r"(?:AROA[A-Z\d]{17}:|\d{12}:assumed-role\/[\w-]*?\/)(\w+)\b")
    """@private"""
    prefix = "sample-role-"
    """@private"""

    def preprocess_match(self, match: re.Match) -> str:
        """@private"""
        return match.group(1)
    
    def generator(self, *args, **kwargs):
        """@private"""
        return generate_name(style="hyphen")
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        if not value.startswith(self.prefix):
            return False
        return True


class RoleNameRule(BaseIdRule):
    """A rule that anonymizes AWS role names."""
    pattern = re.compile(r"role\/([\w-]+)\b")
    """@private"""
    prefix = "sample-role-"
    """@private"""

    def preprocess_match(self, match: re.Match) -> str:
        """@private"""
        return match.group(1)
    
    def generator(self, *args, **kwargs):
        """@private"""
        return generate_name(style="hyphen")
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        if not value.startswith(self.prefix):
            return False
        return True


class InstanceIdRule(BaseIdRule):
    """A rule that anonymizes EC2 instance IDs."""
    pattern = re.compile(r"\bi-[a-fA-F\d]{17}\b")
    """@private"""
    prefix = "i-"
    """@private"""
    length = 17
    """@private"""


class ShortTermAccessKeyIdRule(BaseIdRule):
    """A rule that anonymizes AWS access key IDs."""
    pattern = re.compile(r"ASIA[A-Z\d]{16}")
    """@private"""
    prefix = "ASIA-MOCKACCESSKEYID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class LongTermAccessKeyIdRule(BaseIdRule):
    """A rule that anonymizes AWS access key IDs."""
    pattern = re.compile(r"AKIA[A-Z\d]{16}")
    """@private"""
    prefix = "AKIA-MOCKACCESSKEYID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""


class PublicKeyIdRule(BaseIdRule):
    """A rule that anonymizes AWS access key IDs."""
    pattern = re.compile(r"APKA[A-Z\d]{16}")
    """@private"""
    prefix = "APKA-MOCKPUBLICKEYID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class ComputerNameRule(BaseIdRule):
    """A rule that anonymizes AWS computer names."""
    pattern = re.compile(r"ip-((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\-?\b){4}\b\.[\w-]+\.compute\.internal")
    """@private"""
    prefix = "sample-computer-name-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class StsServiceBearerTokenIdRule(BaseIdRule):
    pattern = re.compile(r"\bABIA\w{16}\b")
    """@private"""
    prefix = "ABIA-MOCKSTSBEARERTOKENID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class ContextSpecificCredentialIdRule(BaseIdRule):
    pattern = re.compile(r"\bACCA\w{16}\b")
    """@private"""
    prefix = "ACCA-MOCKCONTEXTCREDENTIALID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class GroupIdRule(BaseIdRule):
    pattern = re.compile(r"\bAGPA\w{17}\b")
    """@private"""
    prefix = "AGPA-MOCKGROUPID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class Ec2InstanceProfileIdRule(BaseIdRule):
    pattern = re.compile(r"\bAIPA\w{17}\b")
    """@private"""
    prefix = "AIPA-AMOCKEC2INSTANCEPROFILEID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class IamUserIdRule(BaseIdRule):
    pattern = re.compile(r"\bAIDA\w{17}\b")
    """@private"""
    prefix = "AIDA-MOCKIAMUSERID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id

class ManagedPolicyIdRule(BaseIdRule):
    pattern = re.compile(r"\bANPA\w{17}\b")
    """@private"""
    prefix = "ANPA-MOCKMANAGEDPOLICYID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class CertificateIdRule(BaseIdRule):
    pattern = re.compile(r"\bASCA\w{17}\b")
    """@private"""
    prefix = "ASCA-MOCKCERTIFICATEID-"
    """@private"""
    length = 1
    """@private"""
    generator = next_numeric_id
    """@private"""

class S3BucketNameRule(BaseIdRule):
    pattern = re.compile(r"\b([\w-]+)\.s3\b|\b\:s3\:{3}([\w-]+)\b")
    """@private"""
    prefix = "sample-bucket-"
    """@private"""

    def preprocess_match(self, match: re.Match) -> str:
        """@private"""
        return match.group(1) or match.group(2)
    
    def generator(self, *args, **kwargs):
        """@private"""
        return generate_name(style="hyphen")
    
    def is_already_anonymized(self, value: str) -> bool:
        """Check if the value is already anonymized. @private"""
        if not value.startswith(self.prefix):
            return False
        return True