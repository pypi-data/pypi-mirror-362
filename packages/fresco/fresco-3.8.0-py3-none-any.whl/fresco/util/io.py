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
#
"""
Utilities for wrapping IO streams. These are used internally by
fresco when parsing wsgi request input streams.
"""
from io import DEFAULT_BUFFER_SIZE

import typing as t


ByteIterator = t.Iterator[bytes]


def io_iterator(fp: t.IO, size=DEFAULT_BUFFER_SIZE, maxlen=-1) -> ByteIterator:
    bytecount = 0
    if maxlen > 0:
        while True:
            r = fp.read(min(maxlen - bytecount, size))
            bytecount += len(r)
            if r == b"":
                return
            yield r
            if bytecount >= maxlen:
                break
    else:
        while True:
            r = fp.read(size)
            if r == b"":
                return
            yield r
