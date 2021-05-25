import enum
import os
import boto3
from dataclasses import dataclass, field
from typing import Optional, Mapping, Any
from swawesomo.aws.events import event
from swawesomo.common.json import decoder
from swawesomo.common.lazy import Lazy

EVENT_SOURCES = Lazy(lambda: decoder(os.environ["EVENT_SOURCES"]))
DETAIL_TYPE = "Account Registry Service"

events_client = Lazy(lambda: boto3.client("events"))


class Source(str, enum.Enum):
    STATUS = "status"
    DDE = "dde_status"


def get_event_bridge(source: Source):
    return event(events_client.value, EVENT_SOURCES[source], DETAIL_TYPE)


@dataclass
class BaseEventModel:
    _type: str = field(init=False)
    _version: str
    status_code: str
    etag: str
    message: str
    timestamp: str
    module: str
    metadata: Optional[Mapping[str, Any]]

    def __post_init__(self):
        self._type = self.__class__.__name__
