import json
from typing import Any, List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.profiles.user_profile import UserProfile
from utils.claude_connector import ClaudeConnector
from utils.string_utils import StringUtils
from utils.utils import Utils


class Ranker:
    """Takes a list of articles and list of preferences by the user, then outputs a ranked ordering"""

    def __init__(self) -> None:
        pass

    def rank_articles_get_ids(
        self, articles: List[str], profile: UserProfile
    ) -> List[int]:
        """Returns the ranking as a list of integers which represent the rank of the article at the same index.
        Example: articles ['A', 'B', 'C'] are input, B is most relevant, then C, then A. The result would then be
        [3,1,2]"""
        article_list_str = StringUtils.create_article_list_string(articles)
        model_response = self._raw_ranking_call(article_list_str, profile.preferences)
        return self._construct_result_from_response(model_response, len(articles))

    def rank_articles_get_ranked_articles(
        self, articles: List[str], profile: UserProfile
    ) -> List[str]:
        """Returns a sorting of the input articles list by rank in decreasing order (highest ranked article first)"""
        ordering = self.rank_articles_get_ids(articles, profile)
        return list(map(lambda i: articles[i], ordering))

    def _raw_ranking_call(
        self, article_list_string: str, preferences: List[str]
    ) -> str:
        preference_list_string = StringUtils.create_preference_list_string(preferences)
        return ClaudeConnector.prompt_claude_sync(
            f"""{HUMAN_PROMPT} You are my trusted personal assistant tasked with helping with my busy life.
            The following is an enumerated list of article headlines <articleList>{article_list_string}</articleList>.
            This is a list of my preferences: {preference_list_string}
            Your task is to rank the articles based on how well they match my preferences. 
            Please output your findings in JSON format as an ordered list of the indices of the articles, sorted by how well they match my interests.
            {AI_PROMPT}
            """,
            10000,
        )

    def _construct_result_from_response(
        self, response: str, num_articles: int
    ) -> List[int]:
        try:
            parsed = json.loads(response)
            self._verify_result(parsed, num_articles)
            return list(map(lambda e: e + 1, parsed))
        except Exception as e:
            print(e)
            raise RankingException("Error when ranking, check backend logs")

    def _verify_result(self, json: Any, num_articles: int):
        if not isinstance(json, List):
            raise TypeError(
                f"Model response is not a list of numbers! - Not a list {json}"
            )
        if not all(json, lambda e: isinstance(e, int)):
            raise TypeError(
                f"Model response is not a list of numbers! - Does not only contain numbers {json}"
            )
        if not Utils.is_list_with_all_numbers_up_to(json, len(num_articles) - 1):
            raise RankingException(
                f"Model response did not contain all article indices when ranking! {json}"
            )


class RankingException(RuntimeError):
    """When anything fails during ranking"""

    pass
