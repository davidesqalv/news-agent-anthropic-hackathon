from dataclasses import dataclass


@dataclass
class Article:
    raw_content: str
    extracted_content: str
    headline: str
    article_content: str
