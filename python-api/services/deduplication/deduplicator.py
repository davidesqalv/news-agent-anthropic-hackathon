import json
from typing import Any, Dict, List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.deduplication.deduplication_result import DeduplicationResult
from utils.claude_connector import ClaudeConnector
from utils.string_utils import StringUtils
from utils.utils import Utils


class Deduplicator:
    """Takes a list of articles and returns a dict of lists. `unique` maps to a list which contains items on the
    list that are unique articles. `duplicate_i` (i is a running index, starting at 0) maps to a list which
    contains items that are covering the same topic and should be merged"""

    def __init__(self) -> None:
        pass

    def deduplicate(self, articles: List[str]) -> DeduplicationResult:
        """Throws a DeduplicationException if anything bad happens"""
        article_list_str = StringUtils.create_article_list_string(articles)
        model_response = self._raw_deduplication_call(article_list_str)
        return self._construct_result_from_response(model_response, len(articles))

    def _construct_result_from_response(
        self, model_response: str, num_articles: int
    ) -> DeduplicationResult:
        try:
            parsed = json.loads(model_response)
            self._verify_response(parsed, num_articles)
            duplicates = []
            i = 0
            while f"duplicates_{i}" in parsed:
                duplicates.append(list(map(lambda e: e + 1, parsed[f"duplicates_{i}"])))
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
            Please output your findings in JSON format, with the `unique` key containing a list of the indices of all articles that have no duplicates, and each topic that is covered by multiple articles should have a key `duplicates_i` with an increasing index `i`. `duplicates_i` contains a list of the indices of articles that are duplicates of each other (for that topic).
            {AI_PROMPT}
            """,
            10000,
        )

    def _verify_response(self, json: Any, num_articles: int):
        if not isinstance(json, Dict):
            raise TypeError(f"Model response is not a dict when deduplicating! {json}")
        unique_indices = []
        duplicates_indices = []
        duplicate_key_numbers = []
        for key in json.keys():
            if key == "unique":
                unique_indices = json["unique"]
            if key.startswith("duplicates_"):
                duplicates_indices.append(json[key])
                duplicate_key_numbers.append(int(key.split("duplicates_")[1]))
            else:
                raise DeduplicationException(
                    f"Unknown key {key} in model response when deduplicating - {json}"
                )
        all_article_numbers = unique_indices + duplicates_indices.flatten()
        if not Utils.is_list_with_all_numbers_up_to(
            all_article_numbers, num_articles - 1
        ):
            raise DeduplicationException(f"Some articles were lost when deduplicating")
        if not Utils.is_list_with_all_numbers_up_to(
            duplicate_key_numbers, len(duplicate_key_numbers) - 1
        ):
            raise DeduplicationException(
                f"Deduplication keys have gaps {duplicate_key_numbers}"
            )


class DeduplicationException(RuntimeError):
    """When anything fails during deduplication"""

    pass
