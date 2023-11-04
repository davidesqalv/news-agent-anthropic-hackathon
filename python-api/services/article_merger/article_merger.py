import json
from typing import Any, List

from anthropic import AI_PROMPT, HUMAN_PROMPT
from services.profiles.user_profile import UserProfile
from utils.claude_connector import ClaudeConnector
from utils.string_utils import StringUtils
from utils.utils import Utils


class ArticleMerger:
    """Takes a list of articles and list of preferences by the user, then outputs a ranked ordering"""

    def __init__(self) -> None:
        pass

    def merge_articles(self, articles_to_merge: List[str]) -> str:
        """Synthesises a new article based on multiple articles covering the same topic."""
        article_list_str = StringUtils.create_article_list_string(articles_to_merge)
        return self._raw_merging_call(article_list_str)

    def _raw_merging_call(self, article_list_string: str) -> str:
        return ClaudeConnector.prompt_claude_sync(
            f"""{HUMAN_PROMPT} You are a neutral journalist who specializes in balanced, succinct summaries of multiple articles covering the same topic.
            The following is an enumerated list of articles covering the same topic <articleList>{article_list_string}</articleList>.
            Your task is to summarize the main points from all articles, with a balanced set of perspectives from all articles, keeping only the most important bits from each.
            {AI_PROMPT}
            """,
            10000,
        )
