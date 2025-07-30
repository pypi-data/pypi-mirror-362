from collections.abc import Mapping
from collections.abc import Iterable
from collections.abc import Callable
from types import TracebackType
from typing import Any
from typing import Optional
import typing as t

import fresco.response # noqa


QuerySpec = t.Union[
    Mapping[str, Any],
    Iterable[tuple[str, Any]]
]
ViewCallable = Callable[..., "fresco.response.Response"]
ExcInfo = tuple[type[BaseException], BaseException, TracebackType]
OptionalExcInfo = Optional[ExcInfo]


HeaderList = list[tuple[str, str]]
HeadersList = HeaderList
WSGIEnviron = dict[str, Any]
WriteCallable = Callable[[bytes], object]
StartResponse = Callable[[str, HeaderList, OptionalExcInfo], WriteCallable]
WSGIApplication = Callable[
    [
        WSGIEnviron,
        StartResponse,
    ],
    Iterable[bytes]
]
