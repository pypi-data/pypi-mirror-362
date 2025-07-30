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
fresco.request
--------------

The :class:`Request` class models an incoming HTTP request, allowing access to
HTTP headers and request data (eg query string or submitted form data).
"""
from urllib.parse import ParseResult
from urllib.parse import quote
from urllib.parse import urlparse
from urllib.parse import urlunparse
from decimal import Decimal
import typing as t
import datetime
import json
import posixpath
import re

from fresco import exceptions
from fresco.cookie import parse_cookie_header
from fresco.multidict import MultiDict
from fresco.defaults import DEFAULT_CHARSET
from fresco.types import QuerySpec
from fresco.util.http import FileUpload
from fresco.util.http import get_body_bytes
from fresco.util.http import get_content_type_info
from fresco.util.http import parse_post
from fresco.util.http import parse_querystring
from fresco.util.urls import normpath
from fresco.util.urls import make_query
from fresco.util.wsgi import environ_to_str
import fresco

__all__ = "Request", "currentrequest"

KB = 1024
MB = 1024 * KB


class _Marker:
    ...


_marker = _Marker()

T1 = t.TypeVar("T1")
T2 = t.TypeVar("T2")


class Request(object):
    """
    Models an HTTP request, given a WSGI ``environ`` dictionary.
    """

    #: Maximum size for application/x-www-form-urlencoded post data, or maximum
    #: field size in multipart/form-data encoded data, not including file
    #: uploads
    MAX_SIZE = 16 * KB

    #: Maximum size for multipart/form-data encoded post data
    MAX_MULTIPART_SIZE = 2 * MB

    #: Support broken IE content-disposition escaping
    IE_CONTENT_DISPOSITION_WORKAROUND = True

    _body_bytes = None
    _parsed_content_type = None
    _form = None
    _files = None
    _query = None
    _cookies = None
    _parsed_url = None
    _now = None

    STATE_ENV_KEY = "fresco._request_state"

    #: WSGI key for the session variable. The default value is configured for
    #: use with `beaker <http://beaker.groovie.org/>`_
    SESSION_ENV_KEY = "beaker.session"

    #: The WSGI environ dict
    environ: t.Dict

    #: Encoding used to decode WSGI parameters, notably PATH_INFO and form data
    default_charset = DEFAULT_CHARSET

    #: The decoder class to use for JSON request payloads
    json_decoder_class = json.JSONDecoder

    #: List of functions to be called at the end of this request's lifecycle
    teardown_handlers: t.List[t.Callable]

    def __init__(self, environ):
        if self.STATE_ENV_KEY in environ:
            self.__dict__ = environ[self.STATE_ENV_KEY]
        else:
            environ[self.STATE_ENV_KEY] = self.__dict__
            self.environ = environ
            self.teardown_handlers = []

    def __str__(self):
        """
        Return a useful text representation of the request
        """
        return "<%s %s %s>" % (self.__class__.__name__, self.method, self.url)

    @property
    def charset(  # type: ignore
        self, parse_charset=re.compile(r";\s*charset=([\w\d\-]+)").search
    ) -> str:
        try:
            return self.environ["fresco.request.charset"]
        except KeyError:
            r = self.default_charset
            ct = self.environ.get("CONTENT_TYPE")
            if ct is not None:
                match = parse_charset(ct)
                if match is not None:
                    r = self.environ["fresco.request.charset"] = match.group(1)
        return r

    @charset.setter
    def charset(self, value):
        self.environ["fresco.request.charset"] = value

    @property
    def form(self):
        """
        Return the contents of submitted form data

        This will return the ``POST`` or ``PUT`` data when available, otherwise
        querystring (``GET``)  data. Querystring data is always available via
        the ``query`` property.
        """
        if self._form is None:
            if self.environ["REQUEST_METHOD"] in {"PUT", "POST"}:
                items, close = parse_post(
                    self.environ,
                    self.environ["wsgi.input"],
                    self.charset,
                    self.MAX_SIZE,
                    self.MAX_MULTIPART_SIZE,
                    ie_workaround=self.IE_CONTENT_DISPOSITION_WORKAROUND,
                )
                if close:
                    self.teardown_handlers.append(close)
                self._form = MultiDict(items)
            else:
                data = environ_to_str(self.environ.get("QUERY_STRING", ""))
                self._form = MultiDict(parse_querystring(data, self.charset))
        return self._form

    @property
    def content_type_encoding(self):
        if self._parsed_content_type is None:
            self._parsed_content_type = get_content_type_info(self.environ)
        return self._parsed_content_type.encoding

    @property
    def content_type(self):
        if self._parsed_content_type is None:
            self._parsed_content_type = get_content_type_info(self.environ)
        return self._parsed_content_type.content_type

    @property
    def body_bytes(self):
        if self._body_bytes is None:
            self._body_bytes = get_body_bytes(self.environ, self.MAX_SIZE)
        return self._body_bytes

    @property
    def body(self):
        body = self.body_bytes
        if body is None:
            return None
        encoding = self.content_type_encoding or self.charset
        try:
            return body.decode(encoding)
        except UnicodeDecodeError:
            raise exceptions.RequestParseError(
                "Payload contains data that could not be decoded using " + encoding
            )

    def get_json(self, *args, **kwargs):
        """
        Return a decoded JSON request body.

        ``*args`` and ``**kwargs`` are passed to the ``JSONDecoder``
        constructor.

        This will try to decode a json string regardless of the mime type sent
        by the client.
        """
        try:
            return self.json_decoder_class(*args, **kwargs).decode(
                self.body  # type: ignore
            )
        except ValueError:
            raise exceptions.RequestParseError("Payload is not valid JSON")

    @property
    def files(self):
        """
        Return a MultiDict of all ``FileUpload`` objects available.
        """
        if self._files is None:
            self._files = MultiDict(
                (k, v) for k, v in self.form.allitems() if isinstance(v, FileUpload)
            )
        return self._files

    @property
    def query(self, environ_to_str=environ_to_str) -> MultiDict:  # type: ignore
        """
        Return a ``MultiDict`` of any querystring submitted data.

        This is available regardless of whether the original request was a
        ``GET`` request.

        Synopsis::

            >>> from fresco import FrescoApp
            >>> with FrescoApp().requestcontext('/?animal=moose') as c:
            ...     c.request.query['animal']
            u'moose'

        This property always returns querystring data, regardless of the
        request method used.
        """
        if self._query is None:
            query = environ_to_str(self.environ.get("QUERY_STRING", ""))
            self._query = MultiDict(parse_querystring(query, self.charset))

        return self._query

    def __getitem__(self, key: str) -> str:
        """
        Return the value of ``key`` from submitted form values.
        """
        v = self.get(key, default=None)
        if v is None:
            raise KeyError(key)
        return v

    @t.overload
    def get(
        self, key: str, default: T1, type: t.Callable[[str], T2] = str
    ) -> t.Union[T1, T2, None]:
        ...

    @t.overload
    def get(self, key: str, *, type: t.Callable[[str], T2]) -> t.Union[T2, None]:
        ...

    @t.overload
    def get(
        self, key: str, *, type: t.Callable[[str], T2] = str, required: t.Literal[True]
    ) -> T2:
        ...

    def get(
        self,
        key: str,
        default=_marker,
        type: t.Callable[[str], T2] = str,
        required: bool = False,
    ):
        """
        Look up ``key`` in submitted form values.

        :param type:
            The type to which the returned result should be converted

            A :class:`fresco.exceptions.BadRequest` error is raised if ``type`` is
            specified and the value cannot be converted to the given type

        :param default:
            The value to return if the key not present.

        :param required:
            If True, a missing key will cause a
            :class:`fresco.exceptions.BadRequest` to be raised.

        """
        value = self.form.get(key, _marker)
        if value is _marker:
            if required:
                raise exceptions.BadRequest()
            if default is _marker:
                return None
            return default

        if type is str:
            return value
        try:
            return type(value)
        except (TypeError, ValueError):
            raise exceptions.BadRequest()

    def getlist(self, key):
        """
        Return a list of submitted form values for ``key``
        """
        return self.form.getlist(key)

    @t.overload
    def getbool(self, key: str) -> t.Union[bool, None]:
        ...

    @t.overload
    def getbool(self, key: str, default: T1) -> t.Union[bool, T1, None]:
        ...

    @t.overload
    def getbool(self, key: str, *, required: t.Literal[True]) -> bool:
        ...

    def getbool(
        self, key: str, default: T1 = _marker, required: bool = False
    ) -> t.Union[bool, T1, None]:
        """
        Return the named key, converted to a bool.
        """
        if required:
            return self.get(key, type=bool, required=True)
        else:
            return self.get(key, default=default, type=bool)

    @t.overload
    def getdecimal(self, key: str) -> t.Union[Decimal, None]:
        ...

    @t.overload
    def getdecimal(self, key: str, default: T1) -> t.Union[Decimal, T1, None]:
        ...

    @t.overload
    def getdecimal(self, key: str, *, required: t.Literal[True]) -> Decimal:
        ...

    def getdecimal(
        self, key: str, default: T1 = _marker, required: bool = False
    ) -> t.Union[Decimal, T1, None]:
        """
        Return the named key, converted to a decimal.Decimal
        """
        if required:
            return self.get(key, type=Decimal, required=True)
        else:
            return self.get(key, default=default, type=Decimal)

    @t.overload
    def getfloat(self, key: str) -> t.Union[float, None]:
        ...

    @t.overload
    def getfloat(self, key: str, default: T1) -> t.Union[float, T1, None]:
        ...

    @t.overload
    def getfloat(self, key: str, *, required: t.Literal[True]) -> float:
        ...

    def getfloat(
        self, key: str, default: T1 = _marker, required: bool = False
    ) -> t.Union[float, T1, None]:
        """
        Return the named key, converted to a float.
        """
        if required:
            return self.get(key, type=float, required=True)
        else:
            return self.get(key, default=default, type=float)

    @t.overload
    def getint(self, key: str) -> t.Union[int, None]:
        ...

    @t.overload
    def getint(self, key: str, default: T1) -> t.Union[int, T1, None]:
        ...

    @t.overload
    def getint(self, key: str, *, required: t.Literal[True]) -> int:
        ...

    def getint(
        self, key: str, default: T1 = _marker, required: bool = False
    ) -> t.Union[int, T1, None]:
        """
        Return the named key, converted to an integer.
        """
        if required:
            return self.get(key, type=int, required=True)
        else:
            return self.get(key, default=default, type=int)

    def __contains__(self, key):
        """
        Return ``True`` if ``key`` is in the submitted form values
        """
        return key in self.form

    @property
    def now(self, now=datetime.datetime.now, utc=datetime.timezone.utc):  # type: ignore
        """
        Return a timezone-aware UTC datetime instance. The value returned is
        guaranteed to be constant throughout the lifetime of the request.
        """
        if self._now:
            return self._now
        self._now = now(utc)
        return self._now

    @property
    def cookies(self):
        """
        Return a :class:`fresco.multidict.MultiDict` of cookies read from the
        request headers::

            >>> from fresco import FrescoApp
            >>> with FrescoApp().requestcontext(
            ...     HTTP_COOKIE='''Customer="WILE_E_COYOTE";
            ...     Part="Rocket_0001";
            ...     Part="Catapult_0032"
            ... ''') as c:
            ...     request = c.request
            ...
            >>> request.cookies.getlist('Customer')
            ['WILE_E_COYOTE']
            >>> request.cookies.getlist('Part')
            ['Rocket_0001', 'Catapult_0032']

        See rfc2109, section 4.4
        """
        if self._cookies is None:
            self._cookies = MultiDict(
                parse_cookie_header(self.environ.get("HTTP_COOKIE", ""))
            )
        return self._cookies

    def get_header(self, name, default=None):
        """
        Return an arbitrary HTTP header from the request.

        :param name: HTTP header name, eg 'User-Agent' or 'If-Modified-Since'.
        :param default: default value to return if the header is not set.

        Headers in the original HTTP request are always formatted like this::

            If-Modified-Since: Thu, 04 Jan 2007 21:41:08 GMT

        However in the WSGI environment they appear as follows::

            {'HTTP_IF_MODIFIED_SINCE': 'Thu, 04 Jan 2007 21:41:08 GMT'}

        This method expects the former style (eg ``If-Modified-Since``) and is
        not case sensitive.
        """
        return self.environ.get("HTTP_" + name.upper().replace("-", "_"), default)

    @property
    def path(self):
        """\
        Return the path component of the requested URL
        """
        return environ_to_str(self.environ["SCRIPT_NAME"] + self.environ["PATH_INFO"])

    @property
    def url(self):
        """\
        Return the full URL, including query parameters.
        """
        return urlunparse(self.parsed_url)

    @property
    def application_url(self):
        """\
        Return the base URL of the WSGI application (up to SCRIPT_NAME but not
        including PATH_INFO or query information).

        Synopsis::

            >>> from fresco import FrescoApp
            >>> with FrescoApp().requestcontext(HTTP_HOST='example.com',
            ...                                 SCRIPT_NAME='/animals',
            ...                                 PATH_INFO='/lion.html') as c:
            ...     c.request.application_url
            u'http://example.com/animals'
        """
        scheme, netloc, path, params, query, frag = self.parsed_url

        return urlunparse(
            (
                scheme,
                netloc,
                quote(self.environ["SCRIPT_NAME"], encoding="latin1"),
                "",
                "",
                "",
            )
        )

    @property
    def parsed_url(self):
        """\
        Return the current URL as a tuple of the form::

            (addressing scheme, network location, path,
             parameters, query, fragment identifier)

        Synopsis::

            >>> from fresco import FrescoApp
            >>> app = FrescoApp()
            >>> with app.requestcontext(
            ...          'https://example.com/animals/view?name=lion') as c:
            ...     c.request.parsed_url  # doctest: +ELLIPSIS
            ParseResult(scheme=u'https', netloc=u'example.com', ...)

        Components are returned as unicode strings
        """
        if self._parsed_url:
            return self._parsed_url

        environ = self.environ
        script_name = quote(self.environ["SCRIPT_NAME"], encoding="latin1")
        path_info = quote(self.environ["PATH_INFO"], encoding="latin1")
        query_string = self.query_string
        scheme = environ["wsgi.url_scheme"]

        try:
            host = environ["HTTP_HOST"]
            if ":" in host:
                host, port = host.split(":", 1)
            else:
                if scheme == "https":
                    port = "443"
                else:
                    port = "80"
        except KeyError:
            host = environ["SERVER_NAME"]
            port = environ["SERVER_PORT"]

        if (scheme == "http" and port == "80") or (scheme == "https" and port == "443"):
            netloc = host
        else:
            netloc = host + ":" + port

        self._parsed_url = ParseResult(
            scheme,
            netloc,
            script_name + path_info,
            "",  # Params
            query_string or "",
            "",  # Fragment
        )
        return self._parsed_url

    @property
    def path_info(self, environ_to_str=environ_to_str) -> str:
        """
        The PATH_INFO value as a string

        Note that PATH_INFO is already unquoted by the server
        """
        try:
            return environ_to_str(self.environ["PATH_INFO"], self.charset)
        except UnicodeDecodeError:
            raise exceptions.BadRequest

    @property
    def script_name(self) -> str:
        """
        The SCRIPT_NAME value as a string

        Note that SCRIPT_NAME is already unquoted by the server
        """
        try:
            return environ_to_str(self.environ["SCRIPT_NAME"], self.charset)
        except UnicodeDecodeError:
            raise exceptions.BadRequest

    @property
    def query_string(self) -> t.Optional[str]:
        """
        The QUERY_STRING value as a string
        """
        return self.environ.get("QUERY_STRING")

    @property
    def referrer(self) -> t.Optional[str]:
        """
        Return the HTTP referer header, or ``None`` if this is not available.
        """
        s = self.environ.get("HTTP_REFERER")
        if s is None:
            return s
        return environ_to_str(s)

    @property
    def method(self):
        """
        Return the HTTP method used for the request, eg ``GET`` or ``POST``.
        """
        return self.environ["REQUEST_METHOD"]

    @property
    def remote_addr(self):
        """
        Return the remote address of the client
        """
        s = self.environ.get("REMOTE_ADDR")
        if s is None:
            return s
        return environ_to_str(s)

    @property
    def session(self):
        """
        Return the session associated with this request.

        Requires a session object to have been inserted into the WSGI
        environment by a middleware application.
        """
        return self.environ.get(self.SESSION_ENV_KEY)

    @property
    def is_secure(self):
        """
        Return ``True`` if the request is served over a secure connection.
        """
        return self.environ["wsgi.url_scheme"] == "https"

    def make_url(
        self,
        scheme: t.Optional[str] = None,
        netloc: t.Optional[str] = None,
        path: t.Optional[str] = None,
        parameters: t.Optional[str] = None,
        query: t.Union[None, str, QuerySpec] = None,
        query_add: t.Union[None, str, QuerySpec] = None,
        query_replace: t.Union[None, str, QuerySpec] = None,
        fragment: t.Optional[str] = None,
        SCRIPT_NAME: t.Optional[str] = None,
        PATH_INFO: t.Optional[str] = None,
        **kwargs,
    ) -> str:
        r"""
        Make a new URL based on the current URL, replacing any of the six
        URL elements (scheme, netloc, path, parameters, query or fragment). The
        current request's query string is not included in the generated URL
        unless you explicitly pass it in.

        :param scheme:      The URL scheme, eg ``http`` or ``https``
        :param netloc:      The netloc portion of the URL, eg 'example.com:80'
        :param path:        The path portion of the URL, eg '/my/page.html'
        :param parameters:  RFC2396 path parameters (see also the stdlib
                            urlparse module)
        :param fragment:    The URL fragment
        :param query:       Query data, as a list of tuples, a dict or a string.
                            If supplied, any query parameters present in the
                            current request's url will be removed.
        :param query_add:   Query parameters to add. If the current url already
                            contains query parameters with the same name, these
                            will be supplemented with the new values.
        :param query_replace: Query parameters to replace. If the current url
                              already contains query parameters with the same
                              name, these will be replaced with the new values.
        :param PATH_INFO:   The PATH_INFO portion of the path. Overrides
                            ``path``
        :param SCRIPT_NAME: The SCRIPT_NAME portion of the path. Overrides
                            ``path``
        :param kwargs:      Any remaining keyword arguments are appended to the
                            querystring
        :rtype: str

        All arguments (other than query related arguments, see examples below)
        must be strings (not bytes).

        Examples:

        Reproduce the request URL::

            >>> from fresco import FrescoApp
            >>> with FrescoApp().requestcontext(HTTP_HOST='example.com',
            ...                                 SCRIPT_NAME='/fruitsalad',
            ...                                 PATH_INFO='/banana',
            ...                                 QUERY_STRING='cream=n') as c:
            ...     request = c.request

            >>> request.make_url(query=request.query)
            u'http://example.com/fruitsalad/banana?cream=n'

        Replace the URL scheme::

            >>> request.make_url(scheme='ftp')
            u'ftp://example.com/fruitsalad/banana'

        Replace the entire path::

            >>> request.make_url(path='/sausages')
            u'http://example.com/sausages'

        Replace just the path_info portion::

            >>> request.make_url(PATH_INFO='/sausages')
            u'http://example.com/fruitsalad/sausages'

        Add a query string::

            request.make_url(query={'portions': '2'}, cherries='n')
            u'http://example.com/fruitsalad/banana?portions=2;cherries='n'

        If a relative path is passed, the returned URL is joined to the old in
        the same way as a web browser would interpret a relative HREF in a
        document at the current location::

            >>> request.make_url(path='kiwi')
            u'http://example.com/fruitsalad/kiwi'

            >>> request.make_url(path='../strawberry')
            u'http://example.com/strawberry'

            >>> request.make_url(path='../../../plum')
            u'http://example.com/plum'

        The ``query`` argument can take a dictionary, a list of ``(name,
        value)`` pairs or any other type convertable to a MultiDict::

            >>> request.make_url(query='a=tokyo&b=milan')
            u'http://example.com/fruitsalad/banana?a=tokyo&b=milan'

            >>> request.make_url(query={'a': 'tokyo', 'b': 'milan'})
            u'http://example.com/fruitsalad/banana?a=tokyo;b=milan'

            >>> request.make_url(query=[('a', 'tokyo'),
            ...                         ('b', 'milan'),
            ...                         ('b', 'paris')])
            u'http://example.com/fruitsalad/banana?a=tokyo;b=milan;b=paris'

        The ``query_add`` and ``query_replace`` arguments add or replace
        values in an existing query string. If either of these is specified
        then the current request's query string (or value of ``query``, if
        specified) will be extended with the given values.
        These arguments take a dict, a list of ``(key, value)`` tuples, or any
        other type convertable to a MultiDict.
        """
        parsed_url = self.parsed_url
        querystr: t.Optional[str] = None

        if path is not None:
            path = quote(path, encoding=self.charset)

            if path[0] != "/":
                path = posixpath.join(posixpath.dirname(parsed_url[2]), path)
                path = posixpath.normpath(path)

        elif SCRIPT_NAME is not None or PATH_INFO is not None:
            if SCRIPT_NAME is None:
                SCRIPT_NAME = self.script_name
            if PATH_INFO is None:
                PATH_INFO = self.path_info
            path = quote(SCRIPT_NAME + PATH_INFO, encoding=self.charset)

        else:
            path = parsed_url[2]

        query_dict = None
        if query_add or query_replace or kwargs:
            if query_add or query_replace:
                query = query if query is not None else parsed_url[4]
            else:
                query = query if query is not None else MultiDict()

            if isinstance(query, str):
                query_dict = MultiDict(parse_querystring(query))
            elif isinstance(query, MultiDict):
                query_dict = query
            else:
                query_dict = MultiDict(query)

            if query_add is not None:
                query_dict.extend(query_add)

            if query_replace is not None:
                query_dict.update(query_replace)

            if kwargs:
                query_dict.update(kwargs)

            querystr = make_query(query_dict)

        elif query is not None:
            if isinstance(query, str):
                querystr = query
            else:
                querystr = make_query(query)

        url = (
            scheme if scheme is not None else parsed_url[0],
            netloc if netloc is not None else parsed_url[1],
            path if path is not None else parsed_url[2],
            parameters if parameters is not None else parsed_url[3],
            querystr,
            fragment,
        )

        return urlunparse(url)

    def resolve_url(self, url, relative="app"):
        """
        Resolve a partially qualified URL in context of the current request.

        :param url:      A url, may be fully or partially qualified
        :param relative: One of 'app' or 'server'
        :return: A fully qualified URL

        Examples::

            >>> from fresco import FrescoApp
            >>> app = FrescoApp()
            >>> with app.requestcontext('http://example.net/foo/bar') as c:
            ...     request = c.request
            ...
            >>> request.resolve_url('/baz')
            'http://example.net/baz'
            >>> request.resolve_url('baz')
            'http://example.net/foo/baz'
            >>> request.resolve_url('http://anotherhost/bar')
            'http://anotherhost/bar'

        The returned URL path will be normalized:

            >>> app = FrescoApp()
            >>> with app.requestcontext('http://example.net/foo/bar') as c:
            ...     c.request.resolve_url('../bar')
            ...
            'http://example.net/bar'

        URLs can be resolved relative to the application's base URL (including
        SCRIPT_NAME) or the server root via the ``relative`` argument::

            >>> from fresco import FrescoApp
            >>> app = FrescoApp()
            >>> with app.requestcontext(SCRIPT_NAME='/foo',
            ...                         PATH_INFO='bar') as c:
            ...     request = c.request
            >>> request.resolve_url('/baz', relative='app')
            'http://localhost/foo/baz'
            >>> request.resolve_url('/baz', relative='server')
            'http://localhost/baz'

        If not specified, application relative paths will be assumed.
        """
        environ = self.environ
        env = environ.get

        if "://" not in url:
            scheme = environ["wsgi.url_scheme"]

            if scheme == "https":
                port = ":" + environ["SERVER_PORT"]
            else:
                port = ":" + environ["SERVER_PORT"]

            if (
                scheme == "http"
                and port == ":80"
                or scheme == "https"
                and port == ":443"
            ):
                port = ""

            parsed = urlparse(url)
            path_info = quote(environ["PATH_INFO"].encode("latin-1"))
            script_name = quote(environ["SCRIPT_NAME"].encode("latin-1"))

            if not path_info or path_info[-1] != "/":
                path_info = path_info[: path_info.rfind("/") + 1]

            if relative == "app":
                path = script_name + normpath(posixpath.join(path_info, parsed[2]))

            else:
                path = posixpath.join(script_name + path_info, parsed[2])

            url = urlunparse(
                (
                    scheme,
                    env("HTTP_HOST", environ["SERVER_NAME"] + port),
                    normpath(path),
                    parsed[3],
                    parsed[4],
                    parsed[5],
                )
            )
        return url


def currentrequest():
    """\
    Return the current value of ``context.request``, or ``None`` if there is no
    request in scope.
    """
    try:
        return fresco.context.request
    except AttributeError:
        return None
