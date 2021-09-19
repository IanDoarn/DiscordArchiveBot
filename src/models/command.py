from enum import Enum


class ProtectionLevel(Enum):
    # OWNER must ne the highest
    USER = 0
    OWNER = 1


class Command:
    name: str
    protected: bool
    protection_level: ProtectionLevel

    def __init__(
            self,
            name: str,
            protected: bool,
            protection_level: ProtectionLevel = ProtectionLevel.USER
    ):
        self.name = name
        self.protected = protected
        self.protection_level = protection_level

    def __eq__(self, other):
        if isinstance(other, ProtectionLevel):
            return self.protection_level.value == other.value
        raise AssertionError(f"Comparison must be between Command and ProtectionLevel: received {type(other)}")
            
    def __gt__(self, other):
        if isinstance(other, ProtectionLevel):
            return self.protection_level.value > other.value
        raise AssertionError(f"Comparison must be between Command and ProtectionLevel: received {type(other)}")

    def __lt__(self, other):
        if isinstance(other, ProtectionLevel):
            return self.protection_level.value < other.value
        raise AssertionError(f"Comparison must be between Command and ProtectionLevel: received {type(other)}")

    def __ne__(self, other):
        if isinstance(other, ProtectionLevel):
            return self.protection_level.value != other.value
        raise AssertionError(f"Comparison must be between Command and ProtectionLevel: received {type(other)}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Name: {self.name} Protected: {self.protected} Level: {self.protection_level}>"
