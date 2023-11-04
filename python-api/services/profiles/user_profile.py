from dataclasses import dataclass
from typing import List


@dataclass
class UserProfile:
    """Represents a user's profile from the DB"""

    preferences: List[str]
