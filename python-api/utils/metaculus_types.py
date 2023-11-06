from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MetaculusDistribution:
    num: int
    avg: float
    var: float


@dataclass
class MetaculusTimeseries:
    t: float
    community_prediction: float
    num_predictions: int
    distribution: MetaculusDistribution


@dataclass
class MetaculusCategory:
    id: str
    url: str
    short_name: str
    long_name: str


@dataclass
class MetaculusPrediction:
    time: str
    raw: float
    val: str

    @property
    def time_ts(self):
        return datetime.fromisoformat(self.time)


@dataclass
class MetaculusSimplifiedHistory:
    community_prediction: MetaculusPrediction


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
    prediction_count: int
    related_questions: List[Any]
    condition: Any
    sub_questions: List[Any]
    has_fan_graph: bool
    projects: Any
    user_vote: int
    status: str  # Enum: I, T or V
    prediction_histogram: List[List[float]]
    prediction_timeseries: List[Dict[str, float]]
    resolution: Optional[float] = None
    community_prediction: Optional[Dict] = None
    metaculus_prediction: Optional[Dict] = None
    number_of_forecasters: Optional[int] = None
    group: Optional[int] = None
    community_absolute_log_score: Optional[float] = None
    metaculus_absolute_log_score: Optional[float] = None
    metaculus_relative_log_score: Optional[float] = None
    my_predictions: Optional[Any] = None
    divergence: Optional[Any] = None
    peer_score: Optional[Any] = None
    baseline_score: Optional[Any] = None
    anon_prediction_count: Optional[int] = None
    description: Optional[str] = None
    description_html: Optional[str] = None
    resolution_criteria: Optional[str] = None
    resolution_criteria_html: Optional[str] = None
    fine_print: Optional[str] = None
    fine_print_html: Optional[str] = None
    user_predictions: Optional[Any] = None
    categories: Optional[List[str]] = None
    closing_bonus: Optional[float] = None
    cp_hidden_weight_coverage: Optional[Any] = None
    considerations: Optional[Any] = None
    shared_with: Optional[List[Any]] = None
    simplified_history: Optional[MetaculusSimplifiedHistory] = None

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
