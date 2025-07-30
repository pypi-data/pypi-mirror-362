# encoding=utf-8
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
Utilities for working with data on the HTTP level
"""

from binascii import hexlify
from collections import namedtuple
from collections import deque
from collections.abc import Collection
from collections.abc import Mapping
from email.header import Header
from email.message import Message
from email.parser import BytesFeedParser
from io import BytesIO
from itertools import chain
from typing import Dict
from typing import Iterator
from typing import Iterable
from typing import List
from typing import Tuple
from typing import Callable
from typing import Union
from typing import Optional
import typing as t
from tempfile import SpooledTemporaryFile
import os
import re
import io

from urllib.parse import unquote_plus
from shutil import copyfileobj

import fresco
from fresco.defaults import DEFAULT_CHARSET
from fresco.exceptions import RequestParseError
from fresco.util.io import io_iterator
from fresco.util.io import ByteIterator
from fresco.util.wsgi import str_to_environ
from fresco.util.contentencodings import ALLOWED_ENCODINGS

KB = 1024
MB = 1024 * KB

#: Data chunk size to read from the input stream (wsgi.input)
CHUNK_SIZE = min(io.DEFAULT_BUFFER_SIZE, 1024)

ParsedContentType = namedtuple("ParsedContentType", "content_type encoding params")

ParsedField = Union["FileUpload", str]

token_pattern = r"[!#-\'*-.0-9A-Z\^-~]+"
quotedstringparts_pattern = r'(?:(\\.)|([^"\\]+))'
quotedstring_pattern = r'"(?:{})*"'.format(quotedstringparts_pattern)
quotedstring_parser = re.compile(r"{}".format(quotedstringparts_pattern))

parameter_parser = re.compile(
    r"\s*"
    r"(?P<name>{token})"
    r"\s*=\s*(?:({token})|({quotedstring}))\s*(?:;|$)".format(
        token=token_pattern, quotedstring=quotedstring_pattern
    )
)


def get_content_type_info(
    environ,
    default_type="application/octet-stream",
    default_encoding="iso-8859-1",
) -> ParsedContentType:
    """
    Read and parse the Content-Type header and return a
    :class:`ParsedContentType` object.
    """
    ct, params = parse_header(environ.get("CONTENT_TYPE", default_type))
    encoding = params.get("charset", default_encoding)
    if encoding is None or encoding.lower() not in ALLOWED_ENCODINGS:
        encoding = default_encoding
    return ParsedContentType(ct, encoding, params)


class TooBig(RequestParseError):
    """
    Request body is too big
    """

    def __init__(self, *args, **kwargs):
        super(TooBig, self).__init__(*args, **kwargs)
        self.response = fresco.Response.payload_too_large()


class MissingContentLength(RequestParseError):
    """
    No ``Content-Length`` header given
    """

    def __init__(self, *args, **kwargs):
        super(MissingContentLength, self).__init__(*args, **kwargs)
        self.response = fresco.Response.length_required()


def parse_parameters(s, preserve_backslashes=False) -> Dict[str, str]:
    """
    Return ``s`` parsed as a sequence of semi-colon delimited name=value pairs.

    Example usage::

        >>> from fresco.util.http import parse_parameters
        >>> parse_parameters('foo=bar')
        {'foo': 'bar'}
        >>> parse_parameters('foo="bar\\""')
        {'foo': 'bar"'}

    The ``preserve_backslashes`` flag is used to preserve IE compatibility
    for file upload paths, which it incorrectly encodes without escaping
    backslashes, eg::

        Content-Disposition: form-data; name="file"; filename="C:\\tmp\\Ext.js"

    (To be RFC compliant, the backslashes should be doubled up).
    """
    remaining = s.strip()
    if remaining == "":
        return {}

    params = {}
    while True:
        m = parameter_parser.match(remaining)
        if m is None:
            raise RequestParseError(
                "{!r}: expected parameter at character {}".format(
                    s, len(s) - len(remaining)
                ),
                content_type="text/plain",
            )
        groups = m.groups()
        name, value_token, value_qs = groups[:3]

        if value_token:
            params[name] = value_token
        else:
            if preserve_backslashes:
                params[name] = value_qs[1:-1]
            else:
                parts = quotedstring_parser.findall(value_qs)
                value = "".join((qp[1] if qp else t) for qp, t in parts)
                params[name] = value

        remaining = remaining[m.end() :]
        if not remaining:
            break

    return params


def parse_header(
    header: Union[str, Header],
    ie_workaround: bool = False,
    _broken_encoding_sniffer=re.compile(r'\\[^"\\]').search,
) -> Tuple[str, Dict[str, str]]:
    """
    Given a header, return a tuple of
    ``(value, {parameter_name: parameter_value}])``.

    Example usage::

        >>> parse_header("text/html; charset=UTF-8")
        ('text/html', {'charset': 'UTF-8'})
        >>> parse_header("multipart/form-data; boundary=-------7d91772e200be")
        ('multipart/form-data', {'boundary': '-------7d91772e200be'})
    """
    if isinstance(header, Header):
        # Python3's email.parser.Parser returns a Header object (rather than
        # a string) for values containing 8-bit characters. These are then
        # replaced by U+FFFD when converting the header to a string
        header = str(header)

    if ";" not in header:
        return header, {}

    preserve_backslashes = ie_workaround and _broken_encoding_sniffer(header)

    value, remaining = header.split(";", 1)
    return (
        value,
        parse_parameters(remaining.strip(), preserve_backslashes=preserve_backslashes),
    )


def parse_querystring(
    data: str,
    charset: Optional[str] = None,
    strict: bool = False,
    keep_blank_values: bool = True,
    unquote_plus=unquote_plus,
) -> List[Tuple[str, str]]:
    """
    Return ``(key, value)`` pairs from the given querystring::

        >>> list(parse_querystring('green%20eggs=ham;me=sam+i+am'))
        [('green eggs', 'ham'), ('me', 'sam i am')]

    :param data: The query string to parse.
    :param charset: Character encoding used to decode values. If not specified,
                    ``fresco.defaults.DEFAULT_CHARSET`` will be used.

    :param keep_blank_values: if True, keys without associated values will be
                              returned as empty strings. if False, no key,
                              value pair will be returned.

    :param strict: if ``True``, a ``RequestParseError`` will be raised on
                   parsing errors.
    """

    if charset is None:
        charset = DEFAULT_CHARSET

    result: List[Tuple[str, str]] = []
    append = result.append
    sep = "&" if "&" in data else ";"

    for item in data.split(sep):
        if not item:
            continue
        try:
            key, value = item.split("=", 1)
        except ValueError:
            if strict:
                raise RequestParseError(f"Bad query field: {item}")
            if not keep_blank_values:
                continue
            key, value = item, ""

        try:
            append((unquote_plus(key, charset), unquote_plus(value, charset)))
        except UnicodeDecodeError:
            raise RequestParseError(f"Invalid {charset} character data")
    return result


def parse_post(
    environ,
    _io: t.IO[bytes],
    default_charset: Optional[str] = None,
    max_size=16 * KB,
    max_multipart_size=2 * MB,
    ie_workaround=True,
) -> Tuple[Iterable[Tuple[str, ParsedField]], Optional[Callable]]:
    """\
    Parse the contents of an HTTP POST request, which may be either
    application/x-www-form-urlencoded or multipart/form-data encoded.

    Returned items are either tuples of (name, value) for simple string values
    or (name, FileUpload) for uploaded files.

    :param max_multipart_size: Maximum size of total data for a multipart form
                               submission

    :param max_size: The maximum size of data allowed to be read into memory.
                     For a application/x-www-form-urlencoded submission, this
                     is the maximum size of the entire data. For a
                     multipart/form-data submission, this is the maximum size
                     of any individual field (except file uploads).
    """
    ct, charset, ct_params = get_content_type_info(
        environ,
        "application/x-www-form-urlencoded",
        default_charset or DEFAULT_CHARSET,
    )

    try:
        content_length = int(environ["CONTENT_LENGTH"])
    except (TypeError, ValueError, KeyError):
        raise MissingContentLength()

    try:
        bytestream = io_iterator(_io, CHUNK_SIZE, maxlen=content_length)
        if ct == "application/x-www-form-urlencoded":
            if content_length > max_size:
                raise TooBig("Content Length exceeds permitted size")
            return (
                parse_querystring(b"".join(bytestream).decode("ASCII"), charset),
                None,
            )
        else:
            if content_length > max_multipart_size:
                raise TooBig("Content Length exceeds permitted size")
            try:
                boundary = ct_params["boundary"]
            except KeyError:
                raise RequestParseError(
                    "No boundary given in multipart/form-data content-type"
                )
            return parse_multipart(
                bytestream,
                boundary.encode("ASCII"),
                charset,
                max_size,
                ie_workaround=ie_workaround,
            )
    except UnicodeDecodeError:
        raise RequestParseError("Payload contains non ascii data")


class PostParser:
    close: t.Optional[Callable] = None

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        items, self.close = parse_post(*self.args, **self.kwargs)
        return items

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.close:
            self.close()


def get_body_bytes(environ, max_size=16 * KB) -> bytes:
    """
    Read a single message body from environ['wsgi.input'], returning a bytes
    object.
    """
    try:
        content_length = int(environ["CONTENT_LENGTH"])
    except (TypeError, ValueError, KeyError):
        raise MissingContentLength()

    if content_length > max_size:
        raise TooBig("Content Length exceeds permitted size")
    return b"".join(io_iterator(environ["wsgi.input"], maxlen=content_length))


class HTTPMessage(Message):
    """
    Represent HTTP request message headers
    """


def parse_multipart(
    stream: ByteIterator, boundary, default_charset, max_size, ie_workaround=True
) -> Tuple[Iterable[Tuple[str, ParsedField]], Optional[Callable]]:
    """
    Parse data encoded as ``multipart/form-data``.
    Return an iterator over tuples of ` (<field-name>, <data>)``, and an
    optional ``close`` function.

    ``data`` will be a string in the case of a regular input field, or a
    ``FileUpload`` instance if a file was uploaded.

    If a ``close`` function is returned, the caller must call it in order to
    close any temporary files created at the end of the request lifecycle.

    :param stream: input stream from which to read data
    :param boundary: multipart boundary string, as specified by the
                     ``Content-Disposition`` header
    :param default_charset: character set to use for encoding, if not specified
                            by a content-type header. In practice web browsers
                            don't supply a content-type header so this needs to
                            contain a sensible value.
    :param max_size: Maximum size in bytes for any non file upload part
    :param ie_workaround: If True (the default), enable a work around for IE's
                          broken content-disposition header encoding.
    """
    boundary_size = len(boundary)
    if boundary_size > 72:
        raise RequestParseError(
            "Malformed boundary string: must be no more than 70 characters, "
            "not counting the two leading hyphens (rfc 2046)"
        )

    assert (
        boundary_size + 4 < CHUNK_SIZE
    ), "CHUNK_SIZE cannot be smaller than the boundary string length + 4"

    peek = next(stream)
    while len(peek) < boundary_size + 4:
        peek += next(stream)

    if peek[0:2] != b"--":
        raise RequestParseError("Malformed POST data: expected two hypens")

    if peek[2 : boundary_size + 2] != boundary:
        raise RequestParseError("Malformed POST data: expected boundary")

    if peek[boundary_size + 2 : boundary_size + 4] != b"\r\n":
        raise RequestParseError("Malformed POST data: expected CRLF")

    stream = chain([peek[boundary_size + 4 :]], stream)
    open_files = set()
    fields = []

    try:
        while True:
            headers, data, stream = _read_multipart_field(stream, boundary, max_size)
            open_files.add(data)
            try:
                _, params = parse_header(
                    headers["Content-Disposition"], ie_workaround=ie_workaround
                )
            except KeyError:
                raise RequestParseError("Missing Content-Disposition header")

            try:
                name = params["name"]
            except KeyError:
                raise RequestParseError("Missing name in Content-Disposition header")

            is_file_upload = "Content-Type" in headers and "filename" in params
            if is_file_upload:
                data.seek(0)
                fu = FileUpload(params["filename"], headers, data)
                fields.append((name, fu))
            else:
                charset = parse_header(headers.get("Content-Type", ""))[1].get(
                    "charset", default_charset
                )
                if data.tell() > max_size:
                    data.close()
                    open_files.remove(data)
                    raise TooBig("Data block exceeds maximum permitted size")
                try:
                    data.seek(0)
                    fields.append((name, data.read().decode(charset)))
                    data.close()
                    open_files.remove(data)
                except UnicodeDecodeError:
                    raise RequestParseError(f"Invalid {charset} character data")

            peek = next(stream)
            if peek[:2] == b"\r\n":
                stream = chain([peek[2:]], stream)
            elif peek == b"--\r\n":
                if next(stream, None) is None:
                    break
                else:
                    RequestParseError("Boundary incorrectly terminated")
            else:
                raise RequestParseError("Boundary incorrectly terminated")
    except Exception:
        for f in open_files:
            f.close()
        raise

    close: Optional[Callable]  # type: ignore
    if open_files:

        def close():
            for f in open_files:
                f.close()

    else:
        close = None  # type: ignore

    return fields, close


def _read_multipart_field(
    stream: ByteIterator, boundary: bytes, max_size: int
) -> Tuple["HTTPMessage", SpooledTemporaryFile, ByteIterator]:
    """
    Read a single part from a multipart/form-data message and return a tuple of
    ``(headers, data, remainder)``.

    Iterator ``iostream`` must be positioned at the start of the header block
    for the field.

    The caller must call ``data.close()`` after consuming the data.

    ``headers`` is an instance of ``email.message.Message``.

    ``data`` is an instance of ``tempfile.SpooledTemporaryFile``.
    """
    output = SpooledTemporaryFile(max_size)
    parser = BytesFeedParser(_factory=HTTPMessage)
    parser._set_headersonly()  # type: ignore

    header_block, remainder, found = read_until(iter(stream), b"\r\n\r\n")

    deque(map(parser.feed, header_block), maxlen=1)
    if not found():
        raise RequestParseError("Incomplete data (expected header)")
    headers = parser.close()

    sep = b"\r\n--" + boundary
    data, remainder, found = read_until(remainder, sep)
    for chunk in data:
        output.write(chunk)

    # Fallen off the end of the input without having read a complete field?
    if not found():
        output.close()
        raise RequestParseError("Incomplete data (expected boundary)")
    output.flush()

    return headers, output, remainder


def read_until(
    stream: Iterator[bytes], delimiter: bytes
) -> Tuple[ByteIterator, ByteIterator, Callable[[], bool]]:
    """
    Return two iterators over byte stream `stream`` and a callable which
    indicates whether the delimiter was found.

    The first iterator yields all data up to ``delimiter``.
    The second iterator generates all remaining data.

    The first iterator must be exhausted before the second is iterated.
    The callable must only be called after the first iterator has been
    exhausted.
    """
    buf = b""
    found: t.Optional[bool] = None

    def _found():
        if found is None:
            raise AssertionError("The first iterator was not exhausted")
        return found

    def read_upto():
        nonlocal buf, found
        dlen = len(delimiter)
        for chunk in chain(stream, [b""]):
            buf += chunk
            is_at_end = chunk == b""
            if len(buf) > dlen + 4096 or is_at_end:
                before, sep, after = buf.partition(delimiter)
                if sep == b"":
                    if is_at_end:
                        found = False
                        yield buf
                        return
                    pos = len(buf) - dlen
                    if pos > 0:
                        yield buf[:pos]
                        buf = buf[pos:]
                else:
                    found = True
                    if before:
                        yield before
                    buf = after
                    return

    def remainder():
        if buf:
            yield buf
        yield from stream

    return read_upto(), remainder(), _found


class FileUpload(object):
    """\
    Represent a file uploaded in an HTTP form submission
    """

    def __init__(self, filename, headers, fileob):
        self.filename = filename
        self.headers = headers
        self.file = fileob

        # UNC/Windows path
        if self.filename[:2] == "\\\\" or self.filename[1:3] == ":\\":
            self.filename = self.filename[self.filename.rfind("\\") + 1 :]

    def save(self, fileob):
        """
        Save the upload to the file object or path ``fileob``

        :param fileob: a file-like object open for writing, or the path to the
                       file to be written
        """
        if isinstance(fileob, str):
            with open(fileob, "wb") as f:
                return self.save(f)

        self.file.seek(0)
        copyfileobj(self.file, fileob)


def encode_multipart(
    data: Optional[
        Union[
            Mapping[str, str],
            Collection[tuple[str, str]],
        ]
    ] = None,
    files: Optional[
        Collection[
            tuple[str, str, str, Union[bytes, t.Iterable[bytes], t.BinaryIO]]
        ]
    ] = None,
    charset="UTF-8",
    **kwargs
) -> tuple[bytes, dict[str, str]]:
    """
    Encode ``data`` using multipart/form-data encoding, returning a tuple
    of ``(<encoded data>, <environ items>)``.

    :param data: POST data to be encoded, either a dict or list of
                 ``(name, value)`` tuples.

    :param charset: Encoding used for any string values encountered in
                    ``data``

    :param files: collection of ``(name, filename, content_type, data)`` tuples.
                    ``data`` may be either a byte string, iterator or
                    file-like object.

    :param kwargs: other data items as keyword arguments
    :returns: a tuple of ``(<encoded_data>, <environ_items>)``,
              where ``encoded_data`` is a BytesIO object
              and ``environ`` is a dict containing the Content-Type and
              Content-Length headers encoded for inclusion in a WSGI environ
              dict.
    """

    if files is None:
        files = []

    data_items: Iterable[tuple[str, str]]
    if data is None:
        data_items = []
    elif isinstance(data, Mapping):
        data_items = iter(data.items())  # type: ignore
    else:
        data_items = data

    data_items = chain(data_items, kwargs.items())

    boundary = b"-------" + hexlify(os.urandom(16))
    alldata = chain(
        ((header_block(k), payload) for k, payload in data_items),
        ((file_header_block(k, fn, ct), payload) for k, fn, ct, payload in files),
    )

    CRLF = b"\r\n"
    post_data = BytesIO()
    post_data.write(b"--" + boundary)
    for headers, payload in alldata:
        post_data.write(CRLF)
        for name, value in headers:
            post_data.write("{0}: {1}\r\n".format(name, value).encode("ascii"))
        post_data.write(CRLF)
        write_payload(post_data, payload, charset)
        post_data.write(b"\r\n--" + boundary)
    post_data.write(b"--\r\n")
    length = post_data.tell()
    post_data.seek(0)
    wsgienv = {
        "CONTENT_LENGTH": str(length),
        "CONTENT_TYPE": str_to_environ(
            "multipart/form-data; boundary=" + boundary.decode("ascii")
        ),
    }

    return (post_data.getvalue(), wsgienv)


def header_block(name):
    return [("Content-Disposition", 'form-data; name="%s"' % (name,))]


def file_header_block(name, filename, content_type):
    return [
        (
            "Content-Disposition",
            'form-data; name="%s"; filename="%s"' % (name, filename),
        ),
        ("Content-Type", content_type),
    ]


def write_payload(stream, data, charset):
    "Write ``data`` to ``stream``, encoding as required"
    if hasattr(data, "read"):
        copyfileobj(data, stream)
    elif isinstance(data, bytes):
        stream.write(data)
    elif isinstance(data, str):
        stream.write(data.encode(charset))
    else:
        raise ValueError(data)
