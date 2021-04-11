from typing import Generic, TypeVar, Union


class BaseFormattedError(Exception):
    fmt = 'An unspecified error occurred'

    def __init__(self, *args, **kwargs):
        msg = self.fmt.format(*args, **kwargs)
        print(msg)
        super().__init__(self, msg)
        self.args = args
        self.kwargs = kwargs
        self.message = msg
        self.status_code: Union[str, int] = 500

    def __str__(self):
        return self.message

T = TypeVar('T')
class BaseGenericError(Generic[T], BaseFormattedError):
    def __init__(self, data: T, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = data
