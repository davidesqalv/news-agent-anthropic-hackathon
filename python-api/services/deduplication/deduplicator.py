import json
from typing import List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.deduplication.deduplication_result import DeduplicationResult
from utils.claude_connector import ClaudeConnector


class Deduplicator:
    """Takes a list of articles and returns a dict of lists. `unique` maps to a list which contains items on the
    list that are unique articles. `duplicate_i` (i is a running index, starting at 0) maps to a list which
    contains items that are covering the same topic and should be merged"""

    def __init__(self) -> None:
        pass

    def deduplicate(self, articles: List[str]) -> DeduplicationResult:
        """Throws a DeduplicationException if anything bad happens"""
        article_list_str = self.create_article_list_string(articles)
        model_response = self._raw_deduplication_call(article_list_str)
        return self._construct_result_from_response(model_response)

    def _create_article_list_string(self, articles: List[str]) -> str:
        return "\n".join(map(lambda x: f"{x[0]+1}. {x[1]}", enumerate(articles)))

    def _construct_result_from_response(
        self, model_response: str
    ) -> DeduplicationResult:
        try:
            parsed = json.loads(model_response)
            duplicates = []
            i = 0
            while f"duplicates_{i}" in parsed:
                duplicates.append(parsed[f"duplicates_{i}"])
                i += 1
            return DeduplicationResult(parsed["unique"], duplicates)
        except Exception as e:
            print(e)
            raise DeduplicationException(
                "Error when constructing result from response, check backend logs"
            )

    def _raw_deduplication_call(self, article_list_str) -> str:
        # TODO prompt engineer this
        return ClaudeConnector.prompt_claude_sync(
            f"""{HUMAN_PROMPT} You are my trusted personal assistant tasked with helping with my busy life.
            The following is an enumerated list of article headlines <articleList>{article_list_str}</articleList>.
            Your task is to find the articles that are covering the same topic, we call them duplicates. 
            Please output your findings in JSON format, with the `unique` key containing a list of the indices of
            all articles that have no duplicates, and each topic that is covered by multiple articles should have a key
            `duplicates_i` with an increasing index `i`. `duplicates_i` contains a list of the indices of articles that are duplicates of
            each other (for that topic).
            {AI_PROMPT}
            """,
            10000,
        )


class DeduplicationException(RuntimeError):
    """When anything fails during deduplication"""

    pass
