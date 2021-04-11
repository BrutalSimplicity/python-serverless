from dataclasses import dataclass, field
from typing import Generic, TypeVar
from .models import BaseModel
from enum import Enum

T = TypeVar('T')

class ContentType(Enum, str):
    JSON = 'application/json'

@dataclass
class EventModel(BaseModel, Generic[T]):
    '''
    This class is based on the cloudevents specification, see cloudevents.io

    CloudEvents is a specification for describing event data in common formats
    to provide interoperability across services, platforms and systems.

    Args:
        id: Identifies the event. Producers MUST ensure that source + id is unique for each distinct event.
        source: Identifies the context in which an event happened.
        type: This attribute contains a value describing the type of event related to the originating occurrence.
        specversion: The version of the CloudEvents specification which the event uses.
        datacontenttype: Content type of data value.
        time: Timestamp of when the occurrence happened (in RFC 3339 format).
        data: Domain-specific information about the event.


    Attributes:
        id: Identifies the event. Producers MUST ensure that source + id is unique for each distinct event.
        source: Identifies the context in which an event happened.
        type: This attribute contains a value describing the type of event related to the originating occurrence.
        specversion: The version of the CloudEvents specification which the event uses.
        datacontenttype: Content type of data value.
        time: Timestamp of when the occurrence happened (in RFC 3339 format).
        data: Domain-specific information about the event.
    '''
    id: str
    source: str
    specversion: str = field(default='1.0', init=False)
    type: str = field(init=False)
    datacontenttype: str = field(default=ContentType.JSON, init=False)
    time: str
    data: T

    def __post_init__(self):
        self.type = self.data.__class__.__name__
