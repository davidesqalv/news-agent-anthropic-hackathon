import os
from typing import Any, List, Optional

import requests

from utils.metaculus_types import MetaculusCategory, MetaculusQuestion


class MetaculusConnector:
    BASE_API_PATH = "https://www.metaculus.com/api2/"

    def __init__(self) -> None:
        pass

    def get_questions_for_topic(self, topic: str, limit: int = 5) -> List[Any]:
        # TODO impl
        pass

    def get_all_categories(self) -> List[MetaculusCategory]:
        # TODO cache this locally on a file
        initial_resp = self._metaculus_api_call("categories?limit=100")
        total_num_categories = initial_resp["count"]
        currently_fetched = len(initial_resp["results"])
        responses = [initial_resp]
        while total_num_categories > currently_fetched:
            cur_resp = self._metaculus_api_call(
                f"categories?limit=100&offset={currently_fetched}"
            )
            currently_fetched += len(cur_resp["results"])
            total_num_categories = cur_resp["count"]
            responses.append(cur_resp)
        categories_raw = [
            item
            for sublist in (map(lambda r: r["results"], responses))
            for item in sublist
        ]
        return list(
            map(
                lambda result: MetaculusCategory(**result),
                categories_raw,
            )
        )

    def get_questions_from_category(
        self, category: str, limit: int = 20
    ) -> List[MetaculusQuestion]:
        # TODO currently gets questions in chronological order, oldest first - invert
        # or maybe sort by popularity/...
        result = []
        next_call = f"questions/?categories={category}"
        while len(result) < limit:
            data = self._metaculus_api_call(next_call)
            if not data["results"]:
                break
            new_questions = list(map(lambda q: MetaculusQuestion(**q), data["results"]))
            result += new_questions
            if len(result) < limit:
                next_call = data["next"][len(MetaculusConnector.BASE_API_PATH) :]
            else:
                result = result[:limit]
        return result

    def get_question_by_id(self, question_id: int) -> Optional[MetaculusQuestion]:
        data = self._metaculus_api_call(f"questions/{str(question_id)}")
        return MetaculusQuestion(**data)

    def _metaculus_api_call(self, path: str) -> Any:
        resp = requests.get(
            MetaculusConnector.BASE_API_PATH + path,
            headers={"Authorization": "Token " + os.environ["METACULUS_API_KEY"]},
        )
        print(resp.json()["results"][0].keys())
        resp.raise_for_status()
        return resp.json()
