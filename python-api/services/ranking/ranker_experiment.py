import json
import re
from collections import defaultdict
from typing import Any, List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.profiles.user_profile import UserProfile
from utils.claude_connector import ClaudeConnector
from utils.string_utils import StringUtils
from utils.utils import Utils


class RankerExperiment:
    """Takes a list of articles and list of preferences by the user, then outputs a ranked ordering. Experimental ver"""

    def __init__(self) -> None:
        pass

    def rank_articles_get_ids(
        self, articles: List[str], profile: UserProfile, k=10
    ) -> List[int]:
        """Returns the ranking as a list of integers which represent the index of the top `k` articles.
        Example: articles ['A', 'B', 'C'] are input, k = 2, B is most relevant, then C, then A. The result would then be
        [1, 2]"""
        interest_to_articles = defaultdict(list)
        for index, article in enumerate(articles):
            model_response = self._raw_ranking_call(article, profile.preferences)
            interest_level = self._extract_interest_level_from_response(model_response)
            interest_to_articles[interest_level].append((article, index))
        output = []
        num_outputs = 0
        for interest_level in sorted(interest_to_articles.keys(), reverse=True):
            for article, index in interest_to_articles[interest_level]:
                if num_outputs < k:
                    output.append(index)
                    num_outputs += 1
                else:
                    return output
        return output

    def rank_articles_get_ranked_articles(
        self, articles: List[str], profile: UserProfile
    ) -> List[str]:
        """Returns a sorting of the input articles list by rank in decreasing order (highest ranked article first)"""
        interest_level = self.rank_articles_get_ids(articles, profile)
        return list(map(lambda i: articles[i], interest_level))

    def _raw_ranking_call(self, article: str, preferences: List[str]) -> str:
        preference_list_string = StringUtils.create_preference_list_string(preferences)
        return ClaudeConnector.prompt_claude_sync(
            f"""{HUMAN_PROMPT} You are my trusted personal assistant tasked with helping with my busy life.
            The following is an article from a newspaper or a newsletter I have subscribed to:
            <article>{article}</article>.
            This is a list of my preferences: {preference_list_string}
            Your task is to assess my potential interest in the article based on how well they match my preferences and how important the news/information in it are. Please indicate your guess of my interest numerically, with 1 for low interest, 2 for medium interest, 3 for high interest. Only respond with that number.
            {AI_PROMPT}
            """,
            10000,
        )

    def _extract_interest_level_from_response(self, response: str) -> int:
        try:
            first_number = int(re.search(r"[1-3]", response).group(0))
            return first_number
        except Exception as e:
            print(e)
            raise RankingExperimentException("Error when ranking, check backend logs")


class RankingExperimentException(RuntimeError):
    """When anything fails during ranking"""

    pass
