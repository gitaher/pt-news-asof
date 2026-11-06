"""Structured tool and task contracts; declarations only."""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Tool(Enum):
    COMPUTE = "compute"


class Task(Enum):
    RUN = "screen-news"


@dataclass
class Article(Output):
    id: Annotated[str, "Unique article ID"]
    canonical_id: Annotated[str, "Shared syndication group"]
    symbols: Annotated[list[str], "Exact case-sensitive ticker tags"]
    published_at: Annotated[str, "Publication timestamp in canonical UTC"]
    available_at: Annotated[str, "First ingestion timestamp in canonical UTC"]


@dataclass
class TaskInput(Output):
    articles: Annotated[list[Article], "Frozen news metadata snapshot"]
    symbols: Annotated[list[str], "Nonempty unique query tickers"]
    cutoff: Annotated[str, "Inclusive UTC decision timestamp"]
    lookback_hours: Annotated[int, "Inclusive publication lookback from cutoff"]


@dataclass
class TaskOutput(Output):
    selected_ids: Annotated[list[str], "Eligible IDs sorted by available_at then id after deduplication"]


TOOLS = {Tool.COMPUTE: (TaskInput, TaskOutput)}
TASKS = {Task.RUN: (TaskInput, TaskOutput)}
