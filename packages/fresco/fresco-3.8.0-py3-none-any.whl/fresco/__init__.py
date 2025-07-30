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
from fresco.request import Request
from fresco.request import currentrequest
from fresco.requestcontext import context
from fresco.response import Response
from fresco.core import FrescoApp
from fresco.core import urlfor
from fresco.defaults import DEFAULT_CHARSET
from fresco.options import Options
from fresco.routing import Route
from fresco.routing import RRoute
from fresco.routing import RouteCollection
from fresco.routing import DelegateRoute
from fresco.routing import routefor
from fresco.routing import ALL_METHODS
from fresco.routing import GET
from fresco.routing import HEAD
from fresco.routing import POST
from fresco.routing import PUT
from fresco.routing import DELETE
from fresco.routing import OPTIONS
from fresco.routing import TRACE
from fresco.routing import CONNECT
from fresco.routing import VERSION_CONTROL
from fresco.routing import REPORT
from fresco.routing import CHECKOUT
from fresco.routing import CHECKIN
from fresco.routing import UNCHECKOUT
from fresco.routing import MKWORKSPACE
from fresco.routing import UPDATE
from fresco.routing import LABEL
from fresco.routing import MERGE
from fresco.routing import BASELINE_CONTROL
from fresco.routing import MKACTIVITY
from fresco.routing import ORDERPATCH
from fresco.routing import ACL
from fresco.routing import SEARCH
from fresco.routing import PATCH
from fresco.routeargs import routearg
from fresco.routeargs import FormArg
from fresco.routeargs import PostArg
from fresco.routeargs import QueryArg
from fresco.routeargs import GetArg
from fresco.routeargs import CookieArg
from fresco.routeargs import SessionArg
from fresco.routeargs import RequestObject
from fresco.routeargs import FormData
from fresco.routeargs import PostData
from fresco.routeargs import QueryData
from fresco.routeargs import GetData
from fresco.middleware import XForwarded
from fresco.subrequests import subrequest
from fresco.subrequests import subrequest_bytes
from fresco.subrequests import subrequest_raw
from fresco.util.common import object_or_404


__version__ = "3.8.0"
__all__ = [
    "Request",
    "currentrequest",
    "context",
    "Response",
    "FrescoApp",
    "urlfor",
    "ALL_METHODS",
    "DEFAULT_CHARSET",
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
    "TRACE",
    "CONNECT",
    "VERSION_CONTROL",
    "REPORT",
    "CHECKOUT",
    "CHECKIN",
    "UNCHECKOUT",
    "MKWORKSPACE",
    "UPDATE",
    "LABEL",
    "MERGE",
    "BASELINE_CONTROL",
    "MKACTIVITY",
    "ORDERPATCH",
    "ACL",
    "SEARCH",
    "PATCH",
    "DelegateRoute",
    "Options",
    "Route",
    "RouteCollection",
    "RRoute",
    "routearg",
    "FormArg",
    "PostArg",
    "QueryArg",
    "GetArg",
    "CookieArg",
    "SessionArg",
    "RequestObject",
    "FormData",
    "PostData",
    "QueryData",
    "GetData",
    "routefor",
    "XForwarded",
    "subrequest",
    "subrequest_bytes",
    "subrequest_raw",
    "object_or_404",
]
