from typing import List

from deduplication_result import DeduplicationResult


class Deduplicator:
    """Takes a list of articles and returns a dict of lists. `unique` maps to a list which contains items on the
    list that are unique articles. `duplicate_i` (i is a running index, starting at 0) maps to a list which
    contains items that are covering the same topic and should be merged"""

    def __init__(self) -> None:
        pass

    def deduplicate(self, articles: List[str]) -> DeduplicationResult:
        pass


class DeduplicationException(RuntimeError):
    """When anything fails during deduplication"""

    pass
