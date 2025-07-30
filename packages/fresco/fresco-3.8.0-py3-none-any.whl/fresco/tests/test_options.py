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
from decimal import Decimal
from tempfile import NamedTemporaryFile
from tempfile import TemporaryDirectory
from unittest.mock import Mock
import contextlib
import os
import pathlib
import sys

import pytest

from fresco.options import Options
from fresco.options import override_options
from fresco.options import parse_key_value_pairs
from fresco.options import dict_from_options


class TestOptions(object):
    def test_options_dictionary_access(self):
        options = Options()
        options["x"] = 1
        assert options["x"] == 1

    def test_options_attribute_access(self):
        options = Options()
        options.x = 1
        assert options.x == 1

    def test_options_raises_AttributeError(self):
        with pytest.raises(AttributeError):
            Options().x

    def test_options_works_with_getattr(self):
        assert getattr(Options(), "x", 1) == 1
        assert getattr(Options({"x": 2}), "x", 1) == 2
        with pytest.raises(AttributeError):
            assert getattr(Options(), "x")

    def test_options_update_from_object(self):
        class Foo:
            a = 1
            b = 2

        options = Options()
        options.update_from_object(Foo())
        assert options == {"a": 1, "b": 2}

    def test_options_update_from_object_loads_underscore_names(self):
        class Foo:
            pass

        options = Options()
        options.update_from_object(Foo(), True)
        assert "__module__" in options

    def test_options_update_from_file(self):
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"a = 1\nb = 2\n")
            tmpfile.flush()

            options = Options()
            options.update_from_file(tmpfile.name)
            assert options == {"a": 1, "b": 2}

    def test_options_update_from_file_has_dunder_file_global(self):
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"a = __file__")
            tmpfile.flush()

            options = Options()
            options.update_from_file(tmpfile.name)
            assert options == {"a": tmpfile.name}

    def test_options_respects_all(self):
        with NamedTemporaryFile() as tmpfile:
            tmpfile.write(b"__all__ = ['a']\n" b"a = 1\n" b"b = 2\n")
            tmpfile.flush()

            options = Options()
            options.update_from_file(tmpfile.name)
            assert options == {"a": 1}

    def test_update_from_file_doesnt_add_module(self):
        with NamedTemporaryFile() as tmpfile:
            options = Options()
            saved_modules = list(sorted(sys.modules.keys()))
            options.update_from_file(tmpfile.name)
            assert list(sorted(sys.modules.keys())) == saved_modules

    def test_options_copy_returns_options(self):
        assert isinstance(Options().copy(), Options)


class TestOverrideOptions:
    def test_override_options_with_object(self):
        options = Options(foo=1)
        with override_options(options, {"foo": 2, "bar": "a"}):
            assert options["foo"] == 2
            assert options["bar"] == "a"
        assert options["foo"] == 1
        assert "bar" not in options

    def test_override_options_with_kwargs(self):
        options = Options(foo=1)
        with override_options(options, foo=2, bar="a"):
            assert options["foo"] == 2
            assert options["bar"] == "a"
        assert options["foo"] == 1
        assert "bar" not in options


class TestLoadKeyValuePairs:
    def test_it_loads_strings(self):
        assert parse_key_value_pairs({}, ["a=b"]) == {"a": "b"}

    def test_it_loads_ints(self):
        assert parse_key_value_pairs({}, ["a=100"]) == {"a": 100}
        assert parse_key_value_pairs({}, ["a=-100"]) == {"a": -100}
        assert parse_key_value_pairs({}, ["a=+100"]) == {"a": 100}
        # leading zero - not treated as an int
        assert parse_key_value_pairs({}, ["a=01"]) == {"a": "01"}

    def test_it_loads_bools(self):
        assert parse_key_value_pairs({}, ["a=true"]) == {"a": True}
        assert parse_key_value_pairs({}, ["a=True"]) == {"a": True}
        assert parse_key_value_pairs({}, ["a=TRUE"]) == {"a": True}
        assert parse_key_value_pairs({}, ["a=false"]) == {"a": False}
        assert parse_key_value_pairs({}, ["a=False"]) == {"a": False}
        assert parse_key_value_pairs({}, ["a=FALSE"]) == {"a": False}

    def test_it_loads_decimals(self):
        assert parse_key_value_pairs({}, ["a=1.2"]) == {"a": Decimal("1.2")}
        assert parse_key_value_pairs({}, ["a=+1."]) == {"a": Decimal("1")}
        assert parse_key_value_pairs({}, ["a=-.1"]) == {"a": Decimal("-0.1")}

    def test_it_ignores_comments(self):
        assert parse_key_value_pairs({}, ["a=1", "b=2 #comment", "#c=3"]) == {
            "a": 1,
            "b": 2,
        }

    def test_it_interpolates(self):
        assert parse_key_value_pairs({}, ["a=${x}"]) == {"a": "${x}"}
        assert parse_key_value_pairs({}, ["a=$x"]) == {"a": "$x"}
        assert parse_key_value_pairs({"x": 1}, ["a=${x}"]) == {"a": 1}
        assert parse_key_value_pairs({"x": 1}, ["a=$x"]) == {"a": 1}
        assert parse_key_value_pairs({}, ["a=1", "b=$a"]) == {"a": 1, "b": 1}


class TestLoadOptions:
    def check_loadoptions(self, tmpdir, files, sources="*", tags=[], expected={}):
        """
        Write the files indicated in ``sources`` to the given temporary directory,

        Create an Options object and populate it from the specified sources/tags.

        Assert that the loaded options is equal to the value of ``expected``.
        """
        t = pathlib.Path(tmpdir)
        for fname in files:
            with (t / fname).open("w", encoding="UTF-8") as f:
                f.write(files[fname])

        @contextlib.contextmanager
        def optionsdir():
            def loadopts(sources="*", tags=[], strict=False, **kw):
                return Options().load(sources, tags, strict=False, **kw)

            saved = os.getcwd()
            os.chdir(t)
            try:
                yield loadopts
            finally:
                os.chdir(saved)

        if expected:
            with optionsdir() as loadopts:
                assert loadopts(sources, tags) == expected
        else:
            return optionsdir()

    def test_it_loads_kvp_files(self, tmpdir):
        self.check_loadoptions(tmpdir, {"a": "x = 2"}, expected={"x": 2})
        self.check_loadoptions(
            tmpdir, {"a": "x = 2\ny = ${x}"}, expected={"x": 2, "y": 2}
        )
        with self.check_loadoptions(tmpdir, {"a": "x = $__FILE__\ny=${x}"}) as loadopts:
            result = loadopts()
            assert result["x"] == result["y"] == str(pathlib.Path(tmpdir) / "a")

    def test_it_loads_json(self, tmpdir):
        self.check_loadoptions(
            tmpdir, {"a.json": '{"a": ["b"]}'}, expected={"a": ["b"]}
        )

    def test_it_loads_py_files(self, tmpdir):
        self.check_loadoptions(tmpdir, {"a.py": "x = 2 * 2"}, expected={"x": 4})

    def test_py_files_have_options_in_namespace(self, tmpdir):
        self.check_loadoptions(
            tmpdir, {"a.py": "options['foo'] = 'bar'"}, expected={"foo": "bar"}
        )

    def test_it_selects_by_tag(self, tmpdir):
        with self.check_loadoptions(
            tmpdir,
            {
                "a.dev.txt": "a = 1",
                "a.staging.txt": "b = 1",
                "a.staging.local.txt": "c = 1",
                "a.dev.local.txt": "d = 1",
                "a.local.txt": "e = 1",
            },
        ) as loadopts:
            assert loadopts("*", ["dev"]) == {"a": 1}
            assert loadopts("*", ["dev", "local"]) == {"a": 1, "d": 1, "e": 1}
            assert loadopts("*", ["staging"]) == {"b": 1}
            assert loadopts("*", ["staging", "local"]) == {
                "b": 1,
                "c": 1,
                "e": 1,
            }
            assert loadopts("*", ["local"]) == {"e": 1}

    def test_it_loads_in_tag_order(self, tmpdir):
        with self.check_loadoptions(
            tmpdir,
            {
                "a": "a = 'a'",
                "a.0-dev.txt": "a = ${a} a.dev",
                "a.local.txt": "a = ${a} a.local",
                "b.dev.txt": "a = ${a} b.dev",
            },
        ) as loadopts:
            assert loadopts("*", ["dev", "local"]) == {"a": "a a.dev b.dev a.local"}
            assert loadopts("*", ["local", "dev"]) == {"a": "a a.local a.dev b.dev"}

    def test_it_loads_in_priority_order(self, tmpdir):
        with self.check_loadoptions(
            tmpdir,
            {
                "a": "a = 'a'",
                "a.100-dev.txt": "a = ${a} a.100-dev",
                "a.local.txt": "a = ${a} a.local",
                "b.dev.txt": "a = ${a} b.dev",
            },
        ) as loadopts:
            assert loadopts("*", ["dev", "local"]) == {"a": "a b.dev a.local a.100-dev"}
            assert loadopts("*", ["local", "dev"]) == {"a": "a a.local b.dev a.100-dev"}

    def test_it_loads_in_priority_order_without_tags(self, tmpdir):
        with self.check_loadoptions(
            tmpdir,
            {
                "a": "a = a",
                "b.100": "a = ${a} b",
                "a.200.txt": "a = ${a} 100",
            },
        ) as loadopts:
            assert loadopts("*") == {"a": "a b 100"}

    def test_it_loads_from_os_environ(self, tmpdir):
        with setenv(a="2"):
            with self.check_loadoptions(tmpdir, {"a.txt": "a = 1"}) as loadopts:
                assert loadopts("*", [], use_environ=False) == {"a": 1}
                assert loadopts("*", [], use_environ=True) == {"a": 2}

    def test_it_calls_callbacks(self, tmpdir):
        with self.check_loadoptions(tmpdir, {"a.txt": "a = 1"}):
            options = Options()
            mock = Mock()
            options.onload(mock)
            options.load(str(pathlib.Path(tmpdir) / "*"))
            assert mock.called

    def test_it_sets_directory(self, tmpdir):
        with self.check_loadoptions(tmpdir, {"a.txt": "a = 1"}) as loadopts:
            with TemporaryDirectory() as tmpdir2:
                os.chdir(tmpdir2)
                assert loadopts("*") == {}
                assert loadopts("*", dir=tmpdir) == {"a": 1}

    def test_it_accepts_a_list_of_filespecs(self, tmpdir):
        self.check_loadoptions(
            tmpdir,
            {"a.txt": "a=1", "b.txt": "b=1"},
            sources=["a.*", "b.*"],
            expected={"a": 1, "b": 1},
        )

    def test_it_substitutes_from_environment_variables(self, tmpdir):
        with setenv(FOO="bar"):
            self.check_loadoptions(
                tmpdir,
                {"a.txt": "a=1", "a.bar.txt": "a=2"},
                tags=["{FOO}"],
                expected={"a": 2},
            )

        with setenv(FOO="baz"):
            self.check_loadoptions(
                tmpdir,
                {"a.txt": "a=1", "a.bar.txt": "a=2"},
                tags=["{FOO}"],
                expected={"a": 1},
            )

    def test_it_allows_missing_environment_variables(self, tmpdir):
        assert "FOO" not in os.environ
        self.check_loadoptions(
            tmpdir,
            {"a.txt": "a=1", "a.bar.txt": "a=2"},
            tags=["{FOO}"],
            expected={"a": 1},
        )


class TestDictFromOptions:
    def test_it_splits_on_prefix(self):
        options = Options(FOO_BAR=1, FOO_BAZ=2, FOO_BAR_BAZ=3, BAR=4)
        assert dict_from_options("FOO_", options) == {"BAR": 1, "BAZ": 2, "BAR_BAZ": 3}

    def test_it_splits_recursively(self):
        options = Options(
            A_A=1,
            A_B_C_D=2,
            A_B_E=3,
            A_F_G_H=4,
            A_I=5,
            J_A=6,
        )
        assert dict_from_options("A_", options, recursive=True) == {
            "A": 1,
            "B": {"C": {"D": 2}, "E": 3},
            "F": {"G": {"H": 4}},
            "I": 5,
        }


@contextlib.contextmanager
def setenv(**kw):
    saved = {k: os.environ[k] for k in kw if k in os.environ}
    os.environ.update(kw)
    yield os.environ
    for k in kw:
        if k in saved:
            os.environ[k] = saved[k]
        else:
            del os.environ[k]
