from typing import Any, Mapping, Optional, Callable
from cloudtools.common.utils import filter_empty_properties
from cloudtools.common.json import encoder
import functools

def sns_message(sns_client: Any, topic_arn: str, subject: Optional[str] = None,
              encoder: Callable[[Any], Any] = encoder):
    def decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result:
                if (isinstance(result, Mapping)):
                    result = filter_empty_properties(result)
                params = {
                    'TopicArn': topic_arn,
                    'Subject': subject,
                    'Message': encoder(result)
                }
                params = filter_empty_properties(params)
                sns_client.publish(**params)

            return result
        return _wrapper
    return decorator
