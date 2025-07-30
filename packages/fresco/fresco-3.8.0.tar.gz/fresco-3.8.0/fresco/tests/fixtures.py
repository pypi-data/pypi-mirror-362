# encoding=UTF-8
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
from fresco import Route
from fresco.routing import GET
from fresco.response import Response

# A unicode path that can't be represented using ASCII encoding
unquoted_unicode_path = "/ø"

# IRI quoted version of the same path. This is the string the server
# would receive as the HTTP Request-URI
quoted_unicode_path = "/%C3%B8"

# WSGI encoded version of the path. This is the string that appears in the
# environ dict.
wsgi_unicode_path = b"/\xc3\xb8".decode("latin1")

# Malformed path, as sent to the server by a non conforming client.
# The code point has been incorrectly encoded in latin-1 instead of
# UTF-8
misquoted_wsgi_unicode_path = b"/\xf8".decode("latin1")


class CBV(object):
    """
    A class based view
    """

    __routes__ = [
        Route("/", GET, "index_html"),
        Route("/page", GET, "view_page"),
        Route("/page2", GET, "view_page", tag="page2"),
    ]

    def __init__(self, s):
        self.s = s

    def index_html(self):
        return Response([self.s])

    def view_page(self):
        return Response([])


def module_level_function():
    """
    A module level function
    """


def wsgi_app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])

    return [b"ok"]
