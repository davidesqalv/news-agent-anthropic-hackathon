import os
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests


class MetaculusConnector:
    def __init__(self) -> None:
        pass

    def get_questions_for_topic(
        self, topic: str, max_num_questions: int = 100
    ) -> List[Any]:
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

    def _metaculus_api_call(self, path: str) -> Any:
        resp = requests.get(
            "https://www.metaculus.com/api2/" + path,
            headers={"Authorization": "Token " + os.environ["METACULUS_API_KEY"]},
        )
        resp.raise_for_status()
        return resp.json()

    # requests.get("https://www.metaculus.com/api2/categories?limit=100", headers={'Authorization':'Token x'})
    # resp = requests.get("https://www.metaculus.com/api2/questions/19308", headers={'Authorization':'Token x'})
    # requests.get("https://www.metaculus.com/api2/questions/?categories=geopolitics&close_time__gt=2023-11-06T17:33:28Z", headers={'Authorization':'Token x'})


@dataclass
class MetaculusCategory:
    id: str
    url: str
    short_name: str
    long_name: str


@dataclass
class MetaculusQuestion:
    active_state: str
    url: str
    page_url: str
    id: int
    author: int
    author_name: str
    title: str
    title_short: str
    group_label: str
    resolution: Optional[float]
    created_time: str  # datetime string
    publish_time: str
    close_time: str
    effected_close_time: str
    resolve_time: str
    possibilities: Dict
    scoring: Dict
    type: str
    user_perms: Any
    weekly_movement: float
    weekly_movement_direction: int
    cp_reveal_time: str
    edited_time: str
    last_activity_time: str
    activity: float
    comment_count: int
    votes: int
    community_prediction: Optional[Dict]
    metaculus_prediction: Optional[Dict]
    number_of_forecasters: Optional[int]
    prediction_count: int
    related_questions: List[Any]
    group: Optional[int]
    condition: Any
    sub_questions: List[Any]
    has_fan_graph: bool
    projects: Any
    community_absolute_log_score: Optional[float]
    metaculus_absolute_log_score: Optional[float]
    metaculus_relative_log_score: Optional[float]
    user_vote: int
    my_predictions: Optional[Any]
    divergence: Optional[Any]
    peer_score: Optional[Any]
    baseline_score: Optional[Any]
    status: str  # Enum: I, T or V
    prediction_histogram: List[List[float]]
    prediction_timeseries: List[Dict[str, float]]

    @property
    def created_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.created_time)

    @property
    def publish_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.publish_time)

    @property
    def close_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.close_time)

    @property
    def effected_close_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.effected_close_time)

    @property
    def resolve_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.resolve_time)

    @property
    def cp_reveal_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.cp_reveal_time)

    @property
    def edited_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.edited_time)

    @property
    def last_activity_time_ts(self) -> datetime:
        return datetime.fromisoformat(self.last_activity_time)


@dataclass
class MetaculusTimeseries:
    t: float
    community_prediction: float
    num_predictions: int
    distribution: MetaculusDistribution


@dataclass
class MetaculusDistribution:
    num: int
    avg: float
    var: float
