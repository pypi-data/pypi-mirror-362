# Copyright 2015 Oliver Cope
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
"""
Utilities for interfacing with WSGI
"""

import logging
from functools import partial
from io import BytesIO
from urllib.parse import unquote
from urllib.parse import urlparse
from typing import List
import typing as t
import sys

from fresco.types import WSGIApplication
from fresco.types import WriteCallable
from fresco.types import OptionalExcInfo
from fresco.types import HeaderList

logger = logging.getLogger(__name__)
T = t.TypeVar("T")


__all__ = [
    "environ_to_str",
    "str_to_environ",
    "environ_to_bytes",
    "bytes_to_environ",
    "StartResponseWrapper",
    "ClosingIterator",
    "make_environ",
]

#: The core keys expected in the WSGI environ dict, as defined by PEP3333
WSGI_KEYS = set(
    [
        "REQUEST_METHOD",
        "SCRIPT_NAME",
        "PATH_INFO",
        "QUERY_STRING",
        "CONTENT_TYPE",
        "CONTENT_LENGTH",
        "SERVER_NAME",
        "SERVER_PORT",
        "SERVER_PROTOCOL",
    ]
)


#: List of standard request header field names
#: Taken from the list available at
#: http://en.wikipedia.org/wiki/List_of_HTTP_header_fields which combines
#: RFC specified headers with commonly used non-standard header names
REQUEST_HEADER_NAMES = {
    "accept": "Accept",
    "accept_charset": "Accept-Charset",
    "accept_encoding": "Accept-Encoding",
    "accept_language": "Accept-Language",
    "accept_datetime": "Accept-Datetime",
    "authorization": "Authorization",
    "cache_control": "Cache-Control",
    "connection": "Connection",
    "cookie": "Cookie",
    "content_length": "Content-Length",
    "content_md5": "Content-MD5",
    "content_type": "Content-Type",
    "date": "Date",
    "expect": "Expect",
    "from": "From",
    "host": "Host",
    "if_match": "If-Match",
    "if_modified_since": "If-Modified-Since",
    "if_none_match": "If-None-Match",
    "if_range": "If-Range",
    "if_unmodified_since": "If-Unmodified-Since",
    "max_forwards": "Max-Forwards",
    "origin": "Origin",
    "pragma": "Pragma",
    "proxy_authorization": "Proxy-Authorization",
    "range": "Range",
    "referer": "Referer",
    "te": "TE",
    "user_agent": "User-Agent",
    "upgrade": "Upgrade",
    "via": "Via",
    "warning": "Warning",
    "common": "Common",
    "field": "Field",
    "x_requested_with": "X-Requested-With",
    "dnt": "DNT",
    "x_forwarded_for": "X-Forwarded-For",
    "x_forwarded_host": "X-Forwarded-Host",
    "x_forwarded_proto": "X-Forwarded-Proto",
    "front_end_https": "Front-End-Https",
    "x_http_method_override": "X-Http-Method-Override",
    "x_att_deviceid": "X-ATT-DeviceId",
    "x_wap_profile": "X-Wap-Profile",
    "proxy_connection": "Proxy-Connection",
}


def environ_to_str(s, enc="UTF-8"):
    """
    Decode a WSGI environ value to a string
    """
    return s.encode("iso-8859-1").decode(enc)


def str_to_environ(s, enc="UTF-8"):
    """
    Return a string encoded for a WSGI environ value

    This returns a 'bytes-as-unicode' string:

    - encode ``s`` using the specified encoding (eg utf8)
    - decode the resulting byte string as latin-1
    """
    return s.encode(enc, "surrogateescape").decode("iso-8859-1")


def unicode_to_environ(s, enc="UTF-8"):
    import warnings

    warnings.warn(
        "unicode_to_environ is deprecated, use environ_to_str instead",
        DeprecationWarning,
    )
    return environ_to_str(s, enc)


def environ_to_bytes(s):
    """
    Decode a WSGI environ value to a bytes object
    """
    return s.encode("latin1")


def bytes_to_environ(s):
    """
    Encode a byte string to a WSGI environ value

    This returns a 'bytes-as-unicode' string.
    """
    return s.decode("latin1")


def getenv(environ, key, default=None):
    """
    Return the named ``key`` from the WSGI environ dict ``environ`` as
    a byte string.
    """
    try:
        return environ[key].encode("ISO-8859-1")
    except KeyError:
        return default


def setenv(environ, key, value):
    """
    Set the named ``key`` to ``value`` in the WSGI environ dict ``environ``.
    Value must be a byte ``str`` and will be encoded according
    to the rules in PEP-3333.
    """
    environ[key] = value.decode("ISO-8859-1")


class StartResponseWrapper(object):
    """\
    Wrapper class for the ``start_response`` callable, allowing middleware
    applications to intercept and interrogate the proxied start_response
    arguments.

    Synopsis::

        >>> def my_wsgi_app(environ, start_response):
        ...     start_response('200 OK', [('Content-Type', 'text/plain')])
        ...     return ['Whoa nelly!']
        ...
        >>> def my_other_wsgi_app(environ, start_response):
        ...     responder = StartResponseWrapper(start_response)
        ...     result = my_wsgi_app(environ, responder)
        ...     print("Got status", responder.status)
        ...     print("Got headers", responder.headers)
        ...     responder.call_start_response()
        ...     return result
        ...
        >>> from flea import Agent
        >>> result = Agent(my_other_wsgi_app).get('/')
        Got status 200 OK
        Got headers [('Content-Type', 'text/plain')]

    See also ``Response.from_wsgi``, which takes a wsgi callable, environ and
    start_response, and returns a ``Response`` object, allowing the client to
    further interrogate and customize the WSGI response.

    Note that it is usually not advised to use this directly in middleware as
    start_response may not be called directly from the WSGI application, but
    rather from the iterator it returns. In this case the middleware may need
    logic to accommodate this. It is usually safer to use
    ``Response.from_wsgi``, which takes this into account.
    """

    def __init__(self, start_response):
        self.start_response = start_response
        self.status = None
        self.headers: List[str] = []
        self.called = False
        self.buf = BytesIO()
        self.exc_info = None

    def __call__(self, status, headers, exc_info=None):
        """
        Dummy WSGI ``start_response`` function that stores the arguments for
        later use.
        """
        self.status = status
        self.headers = headers
        self.exc_info = exc_info
        self.called = True
        return self.buf.write

    def call_start_response(self):
        """
        Invoke the wrapped WSGI ``start_response`` function.
        """
        try:
            write = self.start_response(self.status, self.headers, self.exc_info)
            write(self.buf.getvalue())
            return write
        finally:
            # Avoid dangling circular ref
            self.exc_info = None


class ClosingIterator(t.Generic[T]):
    """
    Wrap a WSGI iterator to allow additional close functions to be called on
    application exit.

    Synopsis::

        >>> class filelikeobject(object):
        ...
        ...     def read(self):
        ...         print("file read!")
        ...         return ''
        ...
        ...     def close(self):
        ...         print("file closed!")
        ...
        >>> def app(environ, start_response):
        ...     f = filelikeobject()
        ...     start_response('200 OK', [('Content-Type', 'text/plain')])
        ...     return ClosingIterator(iter(f.read, ''), f.close)
        ...
        >>> from flea import Agent
        >>> m = Agent(app).get('/')
        file read!
        file closed!

    """

    __slots__ = ("_iterable", "_next", "_close_funcs", "_closed")

    def __init__(self, iterable: t.Iterable[T], *close_funcs: t.Callable[[], None]):
        """
        Initialize a ``ClosingIterator`` to wrap iterable ``iterable``, and
        call any functions listed in ``*close_funcs`` on the instance's
        ``.close`` method.
        """
        self._iterable = iterable
        self._next = partial(next, iter(iterable))
        self._close_funcs = close_funcs
        iterable_close = getattr(self._iterable, "close", None)
        if iterable_close is not None:
            self._close_funcs = (iterable_close,) + close_funcs
        self._closed = False

    def __iter__(self):
        """
        ``__iter__`` method
        """
        return self

    def __next__(self):
        """
        Return the next item from the iterator
        """
        return self._next()

    def close(self):
        """
        Call all close functions listed in ``*close_funcs``.
        """
        for func in self._close_funcs:
            try:
                func()
            except Exception:
                logger.exception(
                    f"ContentIterator close function {func!r} raised an exception"
                )
        self._closed = True

    def __del__(self):
        """
        Emit a warning if the iterator is deleted without ``close`` having been
        called.
        """
        if not self._closed:
            try:
                import warnings
            except ImportError:
                return
            else:
                warnings.warn("%r deleted without close being called" % (self,))


def make_environ(url="/", environ=None, wsgi_input=b"", **kwargs):
    """
    Return a WSGI environ dict populated with values modelling the specified
    request url and data.

    :param url: The URL for the request,
                eg ``/index.html`` or ``/search?q=foo``.
                Note that ``url`` must be properly URL encoded.
    :param environ: values to pass into the WSGI environ dict
    :param wsgi_input: The input stream to use in the ``wsgi.input``
                        key of the environ dict
    :param kwargs: additional keyword arguments will be passed into the
                    WSGI request environment
    """
    url = urlparse(url)
    netloc = url.netloc
    user = ""
    if "@" in netloc:
        user, netloc = netloc.split("@", 1)

    if ":" in user:
        user = user.split(":")[0]

    if isinstance(wsgi_input, bytes):
        wsgi_input = BytesIO(wsgi_input)

    env_overrides = environ or {}
    for key, value in kwargs.items():
        key = key.replace("wsgi_", "wsgi.")
        if "." not in key:
            if value is None:
                continue
            # Convert core WSGI keys to upper case
            if key.upper() in WSGI_KEYS:
                key = key.upper()
            # Convert header names to form HTTP_USER_AGENT
            elif key.lower() in REQUEST_HEADER_NAMES:
                key = "HTTP_" + key.upper()
            # value must be a python native str, whatever that means
            if not isinstance(value, str):
                value = str_to_environ(value)
        env_overrides[key] = value

    environ = {
        "REQUEST_METHOD": "GET",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "SERVER_PROTOCOL": "HTTP/1.0",
        "HTTP_HOST": netloc or "localhost",
        "SCRIPT_NAME": "",
        "PATH_INFO": str_to_environ(unquote(url.path)),
        "REMOTE_ADDR": "127.0.0.1",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": url.scheme or "http",
        "wsgi.input": wsgi_input,
        "wsgi.errors": sys.stderr,
        "wsgi.multithread": True,
        "wsgi.multiprocess": True,
        "wsgi.run_once": False,
    }
    if url.scheme == "https":
        environ["HTTPS"] = "on"
        environ["SERVER_PORT"] = "443"

    if user:
        environ["REMOTE_USER"] = user

    if url.query:
        environ["QUERY_STRING"] = url.query

    environ.update(env_overrides)
    for k, v in kwargs.items():
        if v is None and "." not in k:
            del environ[k]
    return environ


def apply_request(
    request, wsgicallable: WSGIApplication
) -> tuple[str, HeaderList, OptionalExcInfo, list[bytes]]:
    """
    Execute ``wsgicallable`` with the given request, exhaust and close the
    content iterator and return the result.
    """

    _start_response_result: list[tuple[str, HeaderList, OptionalExcInfo]] = []

    def start_response(
        status: str, headers: HeaderList, exc_info: OptionalExcInfo = None
    ) -> WriteCallable:
        _start_response_result.append((status, headers, exc_info))
        return lambda s: None

    contentiter = wsgicallable(request.environ, start_response)
    assert len(_start_response_result) == 1
    content = list(contentiter)
    if hasattr(contentiter, "close"):
        contentiter.close()  # type: ignore
    return _start_response_result[0] + (content,)
