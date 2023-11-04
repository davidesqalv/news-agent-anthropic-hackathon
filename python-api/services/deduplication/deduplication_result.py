from dataclasses import dataclass
from typing import List, Set


@dataclass
class DeduplicationResult:
    """Class that encapsulates the result of a deduplication request.
    `unique_articles` contains the indices of all articles about unique topics
    `duplications` contains sets of indices of all articles that are duplicates of each other
    """

    unique_articles: List[int]
    duplications: List[List[int]]

    def get_unique_articles(self, articles: List[str]) -> List[str]:
        return list(map(lambda i: articles[i], self.unique_articles))

    def get_duplicated_articles(self, articles: List[str]) -> List[List[str]]:
        return list(
            map(lambda l: list(map(lambda i: articles[i], l)), self.duplications)
        )
