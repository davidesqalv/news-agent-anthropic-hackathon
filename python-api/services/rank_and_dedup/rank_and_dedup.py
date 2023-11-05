import json
from typing import Any, List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.profiles.user_profile import UserProfile
from utils.claude_connector import ClaudeConnector
from utils.string_utils import StringUtils
from utils.utils import Utils


class RankAndDedup:
    """Experimental: Try ranking and deduplicating in one prompt. Takes a list of full articles and user interests, spits out top k deduplicated results."""

    def __init__(self) -> None:
        pass

    def rank_and_deduplicate(
        self,
        articles: List[str],
        profile: UserProfile,
        num_requested_articles: int = 10,
    ) -> str:
        """Returns the ranking as a list of integers which represent the rank of the article at the same index.
        Example: articles ['A', 'B', 'C'] are input, B is most relevant, then C, then A. The result would then be
        [3,1,2]"""
        article_list_str = StringUtils.create_article_list_string(articles)
        return self._raw_rank_and_dedup_call(
            article_list_str, profile.preferences, num_requested_articles
        )

    def _raw_rank_and_dedup_call(
        self,
        article_list_string: str,
        preferences: List[str],
        num_requested_articles: int,
    ) -> str:
        preference_list_string = StringUtils.create_preference_list_string(preferences)
        return ClaudeConnector.prompt_claude_sync(
            f"""{HUMAN_PROMPT} You are my trusted personal assistant tasked with helping with my busy life.
            The following is an enumerated list of articles <articleList>{article_list_string}</articleList>.
            This is a list of my preferences: {preference_list_string}
            Your task is to rank the articles based on how well they match my preferences. If two or more articles ever cover the same topic, summarize their most important points into a single, balanced article.
            Please output the {num_requested_articles} full articles (or the summary of multiple) that best match my interests. Format it as HTML with headings.
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
            raise RankAndDedupException(
                "Error when rank-and-deduping, check backend logs"
            )


class RankAndDedupException(RuntimeError):
    pass
