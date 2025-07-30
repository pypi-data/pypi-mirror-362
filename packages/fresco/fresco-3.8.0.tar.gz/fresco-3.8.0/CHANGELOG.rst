Changelog
=========

3.8.0 (released 2025-07-17)
---------------------------

- Add Response.bad_request ``message`` argument
- Add warnings when loading option files creates undefined keys

3.7.0 (released 2025-05-05)
---------------------------

- Add a ``fresco.util.url.add_query`` function

3.6.0 (released 2025-05-03)
---------------------------

- Replace ``fresco.DEFAULT_CHARSET`` with ``fresco.defaults.DEFAULT_CHARSET``
- Add a ``required`` argument to Request.get
- Add new request.get* functions: ``getfloat``, ``getbool`` and ``getdecimal``

3.5.0 (released 2025-02-25)
---------------------------

- Refactor middleware.XForwarded to clean up error tracebacks and add a new ``force_https`` option
- Add new ``fresco.options.override_options`` function to aid testing
- Automatically add a ``request`` argument where the routed function's first
  positional parameter is annotated as type ``fresco.request.Request``.
  view

3.4.0 (released 2024-10-16)
---------------------------

- Add new ``ALL`` shortcut method, allowing all HTTP methods to be routed to a
  view

3.3.4 (released 2024-08-06)
---------------------------

- Bugfix: ensure option files are loaded in a well defined order

3.3.3 (released 2024-05-01)
---------------------------

- Bugfix: request.now returns the correct time on non-UTC systems
- Add support for Python 3.12 and drop support for 3.8

3.3.2 (released 2023-05-31)
---------------------------

- Bugfix: a fresco app routed through route_wsgi now receives a fresh request
  and environ dict, isolated from the containing app.

3.3.1 (released 2023-05-18)
---------------------------

- The ``route_wsgi`` and ``route_all`` methods now only match at a
  path separator boundary (``'/'``).
- Bugfix: subrequest now works with views routed via ``RRoute`` (and so expect
  an initial ``request`` argument)

3.3.0 (released 2023-05-02)
----------------------------

- Options: fresco.options.Options can now take a list of paths as its first argument
- Options: tags can now be specified with environment variable substitutions
  (eg "{FOO}" would load files tagged with the current value of the 'FOO'
  environment variable)
- Options: add ``fresco.options.list_from_str`` and ``fresco.options.dict_from_options``

3.2.0 (released 2023-04-16)
---------------------------

- Bugfix: fixed cases where the close methods of WSGI content iterators were
  not called, notably when using subrequests
- Bugfix: fix ``ResourceWarnings`` caused by unclosed temporary files
- Added ``route_class`` argument to ``RouteCollection.route``
- Modified ``RouteCollection.route_wsgi`` to allow it to take a string path to
  the WSGI callable instead of the callable itself, making its signature more
  consistent with ``RouteCollection.route``
- Added ``fresco.process_request_once``
- ``request.make_url`` and ``fresco.util.url.make_query`` now drop items from
  the generated query string if the value is ``None``

3.1.0 (released 2022-05-04)
---------------------------

- Bugfix: passing URL paths to subrequests no longer raises an exception
- Added an ``_env`` argument to ``fresco.subrequest.subrequest`` to allow custom
  WSGI environ keys to be passed to the subrequest

3.0.0 (released 2022-05-02)
---------------------------

- Query string generation now defaults to using '&' as a separator
- ``RouteCollection.get_routes`` has been renamed to
  ``RouteCollection.get_route_traversals``
- ``FrescoApp.get_response`` has been changed to require ``request``,
  ``path`` and ``method`` arguments
- ``FrescoApp.get_methods`` has been changed to require ``request`` and
  ``path`` arguments
- ``fresco.subrequests.subrequest`` now copies the current WSGI environ when
  creating new request contexts, ensuring all headers etc are available to the
  subrequest
- Bugfix: ``Route.fallthrough_on`` no longer returns a 404 when a route was
  matched but fell through
- Bugfix: fixed exception on trailing-slash redirects when no PATH_INFO is
  present
- Added ``Response.error``, returning a ``500 Internal Server Error``
  response
- Added ``Response.unauthorized`` and ``Response.unauthorized_basic``
  returning ``401 Unauthorized`` responses
- Added a ``provide_request`` argument to ``fresco.routing.Route`` and the
  related ``RouteCollection.route`` method.
- New parser for multipart/form-data requests
- Performance improvements

2.2.1 (released 2021-05-17)
---------------------------

- Bugfix: fix use of getattr with ``fresco.options.Options``

2.2.0 (released 2021-02-13)
---------------------------

- Added a ``provide_request`` attribute to the ``Route`` class
- Added a ``dir`` argument to ``Options.load``
- Added a ``type`` argument to ``request.get``
  (eg ``limit = request.get('limit', type=int)``)
- Bugfix: the  ``fallthrough_on`` argument to ``RouteCollection.include`` now
  accepts a sequence of status, matching the behaviour of ``Route``.

2.1.0 (released 2020-12-06)
---------------------------

- Added ``fresco.options.Options.load``, a framework for loading options from
  files and environment variables

2.0.4 (released 2020-09-30)
---------------------------

- Bugfix: reinstate ``__file__`` global when loading options via
  ``Options.update_from_file()``

2.0.3 (released 2020-09-27)
---------------------------

- Bugfix: fix DeprecationWarning in ``fresco.options``

2.0.2 (released 2020-08-21)
---------------------------

- Updated documentation

2.0.1 (released 2020-08-06)
---------------------------

- Bugfix: ``is_safe_url`` (and hence ``Response.redirect``) now correctly
  handle port numbers in the netloc part of the URL.

2.0.0 (released 2020-08-05)
---------------------------

- Response.redirect now protects against open redirects (**may be backwards
  incompatible**: if your application requires the old behavior, switch to
  ``Response.unrestricted_redirect``)
- Support for the ``SameSite`` attribute of cookies, defaulting to ``Lax``
- Added ``Request.now`` (returns a datetime instance, constant for the lifetime of the request)
- Added ``Request.getint``
- In ``fresco.util.wsgi``, renamed ``environ_to_unicode`` to
  ``environ_to_str``, and ``unicode_to_environ`` to ``str_to_environ``, to
  reflect the fact that these no longer return or consume unicode objects. The
  old names are still available, but deprecated.

1.0.1 (released 2019-11-26)
---------------------------

- Bugfix: removed an invalid check on HTTP boundary values that was causing
  compatibility issues with some HTTP clients

1.0.0 (released 2019-09-03)
---------------------------

- Dropped Python 2.x compatibility
- Added type hints
- Fix error in request.make_url when passed a dictionary of query values.
- Allow multipart/form-encoded data boundaries to start with characters other
  than '--' for compatibility with a wider range of HTTP clients
- ClosingIterator objects now use __slots__ for improved performance


0.9.0 (released 2019-06-04)
---------------------------

- Accept X-Forwarded-Proto=https as well as X-Forwarded-SSL=on in
  fresco.middleware.XForwarded as an indication that the application is being
  served under https.

0.8.3 (released 2018-06-07)
---------------------------

- Changed how request state is managed for improved compatibility when
  subclassing ``fresco.request.Request``

0.8.2 (released 2018-03-22)
---------------------------

- Bugfix: fixed handling of the the 'middleware' argument to
  `FrescoApp.requestcontext`

0.8.1 (released 2017-10-25)
---------------------------

- New supported platforms: python 3.6, pypy and pypy3
- Added ``util.urls.is_safe_url``
- Added ``Route.fallthrough_on``, allowing your routing configuration to ignore
  responses based on status (eg 404) and fall through to the next configured
  view.

0.8.0 (released 2017-04-26)
---------------------------

- The first ``FrescoApp.process_exception`` handler that returns a value
  terminates exception processing, and that value is returned or re-raised (in
  previous versions processing would continue until all ``process_exception``
  handlers had been called)
- Bugfix: fixed non-dynamic DelegateRoutes used with objects where routes
  reference the views by name.
- Various performance optimizations

0.7.3 (released 2016-11-01)
---------------------------

- Bugfix: fixed an issue where the route cache was not correctly resetting
  exception information, causing spurious routing exceptions to be raised.

0.7.2 (released 2016-09-27)
---------------------------

- Bugfix: multipart form data parsing has been made RFC compliant with
  respect to quoted-strings and backslash escaped characters.
- The spelling of 'process_response_handers' has been corrected to
  'process_response_handlers'.


0.7.1 (released 2016-04-10)
---------------------------

- Bugfix: the return value of the start_response callable passed to middleware
  layers when using ``FrescoApp.requestcontext`` now correctly returns a
  callable.


0.7.0 (released 2016-02-25)
---------------------------

- fresco.static.serve_file no longer adds a default charset header to
  text files.
- fresco.static.serve_file may take arbitrary keyword args, which are passed to
  the Response constructor.
- Bugfix: date formatting in Set-Cookie headers is now RFC conformant
- Exceptions are no longer logged if any process_exception handler returns
  a value.
- Bugfix: a WSGI app mounted via route_wsgi is now passed a value
  for ``SCRIPT_NAME`` that corresponds to its mount point, rather than that of
  the application.

0.6.2 (released 2016-01-21)
---------------------------

- Bugfix: a process_exception handler returning an exc_info tuple was not
  causing the exception to be reraised if other process_exception handlers
  were registered after it.

0.6.1 (released 2016-01-03)
---------------------------

- Error handling: add a mechanism for process_exception handlers to
  reraise the original exception.

0.6.0 (released 2015-10-14)
---------------------------

- Performance: RouteCollection caches route lookups for faster routing
- Bugfix: ResponseExceptions raised during route traversal are now
  correctly handled
- Views may be specified as strings when constructing routes (eg
  ``Route('/', GET, 'myapp.views.homepage')``.
- Route.decorate and Route.filter may now only take a single decorator/filter
  function. Any additional args will be passed to the filter function
  (eg ``Route(...).filter(render, 'index.html')`` will now result in
  the render function being called with an initial positional argument of
  ``'index.html'``, followed by the return value of the view function)
- ``Route.decorate`` and ``Route.filter`` may also be used as function
  decorators.
- Added ``fresco.subrequests`` to help embedding the output of one view within
  another.


0.5.7 (released 2015-09-11)
---------------------------

- RouteCollection now implements the MutableSequence abc.
- Bugfix: parsing multipart/form-data request bodies containg 8-bit headers
  no longer raises an exception

0.5.6 (released 2015-08-11)
---------------------------

- Cache route lookups that result in RouteNotFound exceptions.
  This provides a significant speedup for applications composed of multiple
  RouteCollections.

0.5.5
-----

- User supplied data is no longer reflected in error messages raised
  from ``fresco.routeargs.RequestArg``. This fixes a potential XSS
  vulnerability affecting versions starting from 0.5.0.

0.5.4
-----

- ``Response.set_cookie`` sets the cookie path to '/' by default
- Added ``Response.delete_cookie`` method
- ``process_http_error_response`` and ``process_exception`` handlers are now
  called for errors raised in middleware layers.

0.5.3
-----

- Added ``FrescoApp.insert_middleware`` and ``FrescoApp.remove_middleware``
  methods.
- Middleware may now be added or removed after the app has already started
  serving requests without raising an exception.
- Using ``process_http_error_response`` handlers to customize non-500
  responses (eg a custom 404 error page) no longer causes fresco to switch to
  handling exceptions internally.
  However installing a custom 500 error handler
  or a ``process_exception`` handler
  will still switch Fresco to handling exceptions.

0.5.2
-----

- Bugfix: Response.buffered no longer sets an incorrect Content-Length header
  when the content contains non-ascii characters.

0.5.1
-----

- The information available in route traversal has been extended.
  `RouteTraversal` objects now contain `traversal_args` and `traversal_kwargs`
  fields storing the args/kwargs extracted from the path during traversal.
  The `collections_traversed` field has been extended with a `route` field
  showing the route that was selected from the collection at each stage of
  traversal.

- `RouteTraversal` objects now have `replace` and `build_path` methods
  that may be used to generate modified path traversals and construct a path::

      >>> from fresco import FrescoApp
      >>> app = FrescoApp()
      >>> @route('/<lang:str>/index.html', GET, homepage, name='home')
      ... def homepage(lang):
      ...     return Response({'fr': 'Bonjour!', 'en': 'Hello!'}[lang])
      ...
      >>> traversal = next(app.get_routes('/fr/index.html'))
      >>> en_traversal = traversal.replace('home', {'lang': 'en'})
      >>> en_traversal.build_path()
      '/en/index.html'

- Bugfix: no longer raises an exception when logging is enabled and the view
  callable does not have a '__name__' attribute

0.5.0
-----

- The signature of ResponseException has changed.

  If a single argument is passed it is used as the response body.
  For example ``raise BadRequest('<h1>Oops!</h1>')`` will generate a response
  with the payload ``<h1>Oops!</h1>``.
  Other keyword arguments are passed to the response object allowing
  arbitrary headers to be set in error response
  (eg ``raise BadRequest(x_error='unspecified error')``).

  A side effect of this is that error messages raised from the functions in
  ``fresco.routeargs`` are now reflected in the response body.

  Note that the ``Redirect``, ``RedirectTemporary``, ``RedirectPermanent`` and
  ``MethodNotAllowed`` exceptions retain their existing behaviour.

- ``fresco.decorators.json_response`` may now be called without arguments, eg::

    @json_response
    def my_view():
      return {'key': 'value'}

- A new ``Response.json`` method has been added to facilitate creating JSON
  encoded responses without the use of a decorator.

- ``fresco.routeargs.JSONPayload`` has been added

- Application logging has been made more helpful

0.4.1
-----

- The ``Secure`` attribute of ``fresco.cookies.Cookie`` no longer takes a
  value. Thanks to Andrew Nelis for the patch.
- `Response.redirect` and `fresco.exceptions.Redirect` can now take a view
  as their first argument, which will be resolved with `urlfor`
  (eg `return Response.redirect(views.edit_widget, id=42)`)

0.4.0
------

- Request.cookies now maps names to values (not cookie objects), simplifying
  cookie handling and bringing us in line with how most other frameworks treat
  cookies.
  **This change breaks backwards compatibility**.
- The ``maxage`` and ``http_only`` arguments to
  ``Cookie.__init__`` and ``Response.add_cookie``
  have been renamed to ``max_age`` and ``httponly`` respectively,
  reflecting the spelling used in the Set-Cookie header
  ('Max-Age' and 'HttpOnly').
  **This change breaks backwards compatibility**.
- Changed ``FrescoApp``'s constructor to have the same signature as
  ``RouteCollection``. You can get the old behavior by using the ``views`` and
  ``path`` keyword arguments.
  **This change breaks backwards compatibility**.
- Removed blinker dependency and associated signals. These were never
  documented and the application hooks added in this version provide a more
  flexible replacement.
  **This change breaks backwards compatibility**.
- Removed the deprecated ``url`` method added to view functions
  **This change breaks backwards compatibility**.

0.3.14
------

- Added ``request.is_secure`` property.
- Added ``filters`` keyword argument to ``Route``.
- Calling ``Response()`` with no arguments now creates a ``204 No Content``
  response.
- Calling ``Response('some string')`` no longer causes the string to be output
  byte-by-byte.
- Added ``Response.add_vary`` method.
- Response cookies have had the ``Version`` attribute removed, bringing them
  in line with RFC6265.
- Added hooks to ``FrescoApp``: ``process_request``, ``process_response``,
  ``process_view``, ``process_exception``, ``process_http_error_response``,
  and ``finish_request``.
- Deprecated blinker signals in ``FrescoApp``.
  ``FrescoApp.route_matched``, ``FrescoApp.view_finished``
  and ``FrescoApp.before_response`` should be
  replaced by the equivalent appliation hooks (``process_request``,
  ``process_view`` and ``process_response`` respectively).

0.3.13
------

- Bugfix for ``FrescoApp.requestcontext_put`` and
  ``FrescoApp.requestcontext_patch`` which were raising a TypeError

0.3.12
------

- Added ``FrescoApp.requestcontext_post``,
  ``FrescoApp.requestcontext_put``,
  ``FrescoApp.requestcontext_patch`` and
  ``FrescoApp.requestcontext_delete``,
  to simplify direct testing of view functions.
- Added a flag to disable middleware processing in requestcontext, eg
  ``FrescoApp.requestcontext(middleware=False)``. For middleware heavy stacks
  this may be used to speed up testing of individual views.

0.3.11
------

- Added ``request.body`` and ``request.body_bytes`` properties
- Added a ``request.get_json`` method to access JSON request payloads
- Deprecated ``view_function.url()``
- Added ``RouteCollection.remove`` and ``RouteCollection.replace`` methods,
  making it easier to extend and modify RouteCollections.

0.3.10
------

- Invalid character data in the request body no longer causes an exception.

0.3.9
-----

- ``fresco.decorators.extract_*`` methods are now deprecated in favour of the
  functions in ``fresco.routeargs``
- Fixed an error in RouteArg when using a conversion function and a value is
  not supplied
- Added ``fresco.decorators.json_response``
- Added support for python 3.4 and dropped support for python 3.2

0.3.8
-----

- A new ``routearg`` function allows RouteArgs to be constructed dynamically
- Renamed ``Route.decorate`` to ``Route.wrap``
- Added ``Route.filter`` to pipe the output of the view through a custom filter
  function


0.3.7
-----

- Bugfix for RouteArg when using a default value
- Bugfix for urlfor when using positional arguments.
- Added decorate method for Route objects.
- Added fresco.routing.register_converter class decorator for simpler
  registration of routing pattern converters.
- Added fresco.util.common.object_or_404.
- Bugfix: fresco.util.urls.make_query no longer sorts key value pairs into
  alphabetical order, but preserves the original ordering.
- fresco.static.serve_static_file now checks for certain malformed requests
  and returns an HTTP bad request status

0.3.6
-----

- Improved startup time for apps with lots of middleware
- fresco.context no longer copies values from the parent when setting up
  a new request context. This makes it easier for libraries using
  fresco.context to cache resources per-request.
- Bugfix for FrescoApp.requestcontext, which was creating duplicate context
  frames.
- FrescoApp.view_finished signal now passes the request object to subscribers
- Route objects can now take a tuple of positional args to pass to views::

      Route(POST, '/contact', args=('anne@example.com',))

- The route class used by RouteCollection is now configurable, allowing apps to
  define custom routing classes.
- fresco.routearg.RouteKwarg has been renamed to ``RouteArg`` and now works for
  positional arguments via ``Route(..., args=...)``
- ``Request.make_url`` now accepts two new optional arguments, ``query_add``
  and ``query_replace``. This facilitates building urls based on the current
  query string with selected values added or replaced.
- Bugfix: improperly encoded paths now cause a 400 bad response to be returned
  rather than raising UnicodeDecodeError

0.3.5
-----

- FrescoApp.requestcontext() now invokes all registered middleware. This can be
  useful for testing views that rely on middleware to set environ keys or
  provide other services

- RouteArg classes have been expanded and are now in a separate module,
  ``fresco.routeargs``

0.3.4
-----

- Bugfix: Request.form was not handling unicode data in GET requests correctly
- fresco.core.request_class has been moved to FrescoApp.request_class
- Route arguments can take default arguments for url generation
- Added tox for testing: fresco is now tested and works with Python 2.6,
  2.7, 3.2 and 3.3

0.3.3
-----

- Bugfix: Request.make_url was double quoting URLs in some circumstances

0.3.2
-----

- Improved handling for ResponseExceptions raised during route traversal

0.3.1
-----

- Bugfix: routing arguments were being incorrectly converted to bytestrings in
  python2
- Bugfix: urlfor works correctly with dynamic routes

0.3.0
-----

**Note that upgrading to this version will require changes to your
application**

- View functions are no longer passed a request object as a positional argument
- The syntax used to reference views by name has changed from
  ``urlfor('mymodule:view')`` to ``urlfor('mymodule.view')``.
- Routing: named routes are now supported, eg ``Route('/', GET, myview,
  name='homepage')``. These can later be accessed by eg ``urlfor('homepage')``.
  The old route tagging facility has been removed.
- Routing: Support for delegating paths to other routeable objects
- fresco.exceptions.NotFoundFinal has been replaced by NotFound(final=True)
- Experimental Python 3 support

0.2.4
-----

- Bugfix: setting the logger property on a FrescoApp no longer causes errors

0.2.3
-----

- FrescoApp objects now have an options dictionary for application level
  settings
- Added serve_static_file function
- Added support for signals with blinker
- urlfor now requires fully qualified module names if called with a string
  argument

0.2.2
-----

- Bug: URL generation broken when HTTP_HOST does not contain port number

0.2.1
-----

- Bugfixes for beaker session support and broken URL generation when
  'X-Forwarded-SSL: off' header supplied

0.2.0
-----

- Removed dependency on Pesto

0.1 (unreleased)
----------------

