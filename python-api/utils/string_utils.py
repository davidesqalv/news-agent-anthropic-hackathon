from typing import List


class StringUtils:
    @classmethod
    def create_article_list_string(cls, articles: List[str]) -> str:
        return "\n".join(map(lambda x: f"{x[0]+1}. {x[1]}", enumerate(articles)))
