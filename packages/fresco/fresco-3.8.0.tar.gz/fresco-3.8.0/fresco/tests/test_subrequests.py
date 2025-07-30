# encoding: UTF-8
from fresco.core import FrescoApp
from fresco.routing import GET
from fresco.routing import Route
from fresco.requestcontext import context
from fresco.response import Response
from fresco.routeargs import GetArg, routearg
from fresco.subrequests import subrequest
from fresco.subrequests import subrequest_bytes
from fresco.subrequests import subrequest_raw
from fresco.subrequests import subrequest_str

from unittest.mock import Mock
import typing as t
import pytest


class TestSubRequest(object):
    def test_it_raises_exception_if_decoding_impossible(self):
        def view_bytes():
            return Response(b"caf\xe9", content_type="text/plain")

        with FrescoApp().requestcontext():
            with pytest.raises(ValueError):
                subrequest(view_bytes)

    def test_it_decodes_response_content(self):
        def view_latin1():
            return Response(
                "café".encode("latin1"),
                content_type="text/plain; charset=Latin-1",
            )

        def view_utf8():
            return Response(
                "café".encode("UTF-8"),
                content_type="text/plain; charset=UTF-8",
            )

        def view_string():
            return Response("café", content_type="text/plain; charset=UTF-8")

        def view_list_of_strings():
            return Response(["café"], content_type="text/plain; charset=UTF-8")

        with FrescoApp().requestcontext():
            assert subrequest(view_utf8) == "café"
            assert subrequest(view_latin1) == "café"
            assert subrequest(view_string) == "café"
            assert subrequest(view_list_of_strings) == "café"

    def test_it_returns_a_markup_string(self):
        def view_html():
            return Response("<html>", content_type="text/html; charset=UTF-8")

        def view_text():
            return Response("text", content_type="text/plain; charset=UTF-8")

        with FrescoApp().requestcontext():
            assert hasattr(subrequest(view_html), "__html__")
            assert not hasattr(subrequest(view_text), "__html__")

    def test_it_returns_raw_response(self):
        r = Response("foo")
        with FrescoApp().requestcontext():
            assert subrequest_raw(lambda: r) is r

    def test_it_returns_content_as_bytes(self):
        def view():
            return Response(
                "café".encode("latin1"),
                content_type="text/plain; charset=Latin-1",
            )

        with FrescoApp().requestcontext():
            assert subrequest_bytes(view) == b"caf\xe9"

    def test_it_calls_response_onclose(self):
        m = Mock()
        r = Response(onclose=m)
        with FrescoApp().requestcontext():
            assert subrequest(lambda: r) == ""
        assert m.call_count == 1

    def test_viewspec_resolves(self):
        def view():
            return Response("foo")

        app = FrescoApp()
        app.route("/view", GET, view, name="named view")
        with app.requestcontext():
            assert subrequest("named view") == "foo"

    def test_viewspec_can_be_a_path(self):
        def view():
            return Response("foo")

        app = FrescoApp()
        app.route("/view", GET, view, name="named view")
        with app.requestcontext():
            assert subrequest("/view") == "foo"

    def test_viewspec_uses_routeargs(self):
        def view(a, b):
            return Response(["*" + a + b + "*"])

        app = FrescoApp()
        app.route("/view", GET, view, a=GetArg(), b=routearg(lambda r: r.method))

        with app.requestcontext("/view?a=foo"):
            assert subrequest(view, _resolve=True) == "*fooGET*"
            assert subrequest(view, _resolve=True, a="bar", b="baz") == "*barbaz*"

    def test_viewspec_resolves_dynamic(self):
        class Views(object):
            def __init__(self, a):
                self.a = a

            def view(self, b):
                return Response("*" + self.a + b + "*")

            __routes__ = [Route("/<b:str>", GET, "view", name="named view")]

        app = FrescoApp()
        app.delegate("/<a:str>", Views, dynamic=True, name="named collection")

        with app.requestcontext():
            assert (
                subrequest("named collection:named view", a="foo", b="bar")
                == "*foobar*"
            )

    def test_it_does_a_full_request(self):
        request_hook = Mock(return_value=None)
        view = Mock(return_value=Response())

        app = FrescoApp()
        app.route("/view", GET, view)
        app.process_request(request_hook)
        with app.requestcontext():
            subrequest(view)
            assert view.call_count == 1
            assert request_hook.call_count == 0

            subrequest(view, _full=True)
            assert view.call_count == 2
            assert request_hook.call_count == 1

    def test_it_maintains_the_environ(self):
        subreq_environ = None

        def view():
            nonlocal subreq_environ
            subreq_environ = context.request.environ
            return Response()

        app = FrescoApp()
        app.route("/view", GET, view)

        with app.requestcontext("/xyzzy") as c:
            original_environ = c.request.environ
            subrequest(view)
            assert subreq_environ is original_environ

    def test_it_passes_original_environ_values(self):
        subreq_environ = None

        def view():
            nonlocal subreq_environ
            subreq_environ = context.request.environ
            return Response()

        app = FrescoApp()
        app.route("/view", GET, view)
        environ_copied = {
            "HTTP_COOKIE": "1234",
            "REMOTE_IP": "192.168.0.1",
            "REMOTE_USER": "username",
        }
        environ_not_copied = {
            "PATH_INFO": "/not-copied",
            "QUERY_STRING": "not-copied",
        }

        with app.requestcontext("/xyzzy") as c:
            original_environ = c.request.environ
            c.request.environ.update(environ_copied)
            c.request.environ.update(environ_not_copied)
            subrequest(view, _full=True, _query="test")
            assert isinstance(subreq_environ, dict)
            assert subreq_environ is not original_environ
            assert all(subreq_environ[k] == environ_copied[k] for k in environ_copied)
            assert all(
                subreq_environ[k] != environ_not_copied[k] for k in environ_not_copied
            )
            assert subreq_environ["PATH_INFO"] == "/view"
            assert subreq_environ["QUERY_STRING"] == "test"

    def test_it_merges_custom_environ_keys(self):
        subreq_environ: t.Optional[dict] = None

        def view():
            nonlocal subreq_environ
            subreq_environ = context.request.environ
            return Response()

        app = FrescoApp()
        app.route("/view", GET, view)

        with app.requestcontext("/xyzzy") as c:
            original_environ = c.request.environ
            subrequest(view, _full=True, _env={"hey.there": True})
            assert subreq_environ is not None
            assert "hey.there" in subreq_environ
            assert "hey.there" not in original_environ

    def test_it_exhausts_content_iterator_before_closing_response(self):
        tracker = ["view inited"]

        def view():
            def responder():
                tracker.append("responder started")
                yield ",".join(tracker)

            r = Response(responder())
            r = r.add_onclose(lambda: tracker.append("response closed"))
            return r

        app = FrescoApp()
        app.route("/", GET, view)

        with app.requestcontext("/"):
            result = subrequest_str(view, _full=True)
        assert ",".join(tracker) == "view inited,responder started,response closed"

        assert result == "view inited,responder started"
