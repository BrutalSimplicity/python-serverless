from typing import Any, Mapping, Callable, List
from cloudtools.common.utils import generate_timestamp, filter_empty_properties
from cloudtools.common.json import encoder
import functools

def event(event_bridge_client: Any, source: str, detail_type: str, event_bus_name: str = None,
          resources: List[str] = [], time: str = generate_timestamp(), encoder: Callable[[Any], Any] = encoder):
    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result:
                if (isinstance(result, Mapping)):
                    result = filter_empty_properties(result)
                entry = {
                    'Source': source,
                    'Detail': encoder(result),
                    'DetailType': detail_type,
                    'EventBusName': event_bus_name,
                    'Resources': resources,
                    'Time': time
                }
                entry = filter_empty_properties(entry)
                event_bridge_client.put_events(
                    Entries=[entry]
                )

            return result
        return _wrapper
    return decorator
