from enum import Enum

class FailMode(str, Enum):
    ANY = "any"      # Fail unless at least one input is present.
    ALL = "all"      # Fail unless at least one input is present.
    NEVER = "never"  # Never fail.