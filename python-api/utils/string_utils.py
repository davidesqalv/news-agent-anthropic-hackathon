from typing import List


class StringUtils:
    @classmethod
    def create_article_list_string(cls, articles: List[str]) -> str:
        return "\n".join(map(lambda x: f"{x[0]+1}. {x[1]}", enumerate(articles)))

    # TODO: Try this out in the ranker/deduplicator
    @classmethod
    def create_article_list_string_experiment(cls, articles: List[str]) -> str:
        if not articles:
            return "There are no articles."
        return (
            "<articleList>\n"
            + "\n  ".join(
                map(
                    lambda x: f"<article>{x[0]+1}. {x[1]}</article>",
                    enumerate(articles),
                )
            )
            + "\n</articleList>"
        )

    @classmethod
    def create_preference_list_string(cls, preferences: List[str]) -> str:
        return (
            ("<preferenceList>I have no preferences.</preferenceList>")
            if not preferences
            else (
                "<preferenceList><preference>"
                + "</preference><preference>".join(preferences)
                + "</preference></preferenceList>"
            )
        )
