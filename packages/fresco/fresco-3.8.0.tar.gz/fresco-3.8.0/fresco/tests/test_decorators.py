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
from fresco.decorators import json_response


class TestJSONResponse(object):
    def test_it_allows_custom_formatting(self):
        r = json_response({"l": [1, 2, 3]}, indent=1, separators=(", ", ": "))
        assert list(r.content_iterator) == [b'{\n "l": [\n  1, \n  2, \n  3\n ]\n}']

    def test_it_acts_as_a_filter(self):
        r = json_response({"l": [1, 2, 3]})
        assert list(r.content_iterator) == [b'{"l":[1,2,3]}']
        assert r.get_header("content-type") == "application/json"

    def test_it_acts_as_a_decorator(self):
        @json_response()
        def f():
            return {"l": [1, 2, 3]}

        assert list(f().content_iterator) == [b'{"l":[1,2,3]}']

    def test_it_acts_as_a_decorator_without_arguments(self):
        @json_response
        def f():
            return {"l": [1]}

        assert list(f().content_iterator) == [b'{"l":[1]}']
