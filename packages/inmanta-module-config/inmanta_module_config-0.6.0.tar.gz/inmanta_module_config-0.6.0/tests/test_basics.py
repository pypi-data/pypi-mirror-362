"""
:copyright: 2022 Inmanta
:contact: code@inmanta.com
:license: Inmanta EULA
"""

import pathlib
import re

import pytest
import yaml
from pytest_inmanta.plugin import Project

import inmanta.ast


def test_get_config_value(project: Project) -> None:
    project.compile(
        """
            import config

            conf = {
                "a": "hah",
                "b": [
                    {
                        "c": 1,
                        "d": true,
                        "e": "aha",
                        "f": null,
                    },
                ],
            }

            # Get a string config value
            assert_a = "hah"
            assert_a = config::get_config_value(conf, "a")
            assert_a = config::get_config_value_as_string(conf, "a")

            # Get an integer config value
            assert_c = 1
            assert_c = config::get_config_value(conf, "b[c=1].c")
            assert_c = config::get_config_value_as_int(conf, "b[c=1].c")

            # Get a boolean config value
            assert_d = true
            assert_d = config::get_config_value(conf, "b[c=1].d")
            assert_d = config::get_config_value_as_bool(conf, "b[c=1].d")
        """,
        no_dedent=False,
    )


def test_resolve_path(project: Project) -> None:
    project.compile(
        f"""
            import config

            project_path = "{project._test_project_dir}"
            module_path = "{pathlib.Path(__file__).parent.parent}"

            # Resolving a system path
            assert_1 = project_path
            assert_1 = config::resolve_path("file://{{{{ project_path }}}}")

            # Resolving a file path in a project
            assert_2 = "{{{{ project_path }}}}/files/test.txt"
            assert_2 = config::resolve_path("inmanta:///files/test.txt")

            # Resolving a template path in a project
            assert_3 = "{{{{ project_path }}}}/templates/test.txt"
            assert_3 = config::resolve_path("inmanta:///templates/test.txt")

            # Resolving a file path in a module
            assert_4 = "{{{{ module_path }}}}/files/test.txt"
            assert_4 = config::resolve_path("inmanta://config/files/test.txt")
            assert_4 = config::resolve_path("source://config/test.txt")

            # Resolving a template path in a module
            assert_5 = "{{{{ module_path }}}}/templates/test.txt"
            assert_5 = config::resolve_path("inmanta://config/templates/test.txt")
            assert_5 = config::resolve_path("template://config/test.txt")
        """,
        no_dedent=False,
    )


def test_load_config(project: Project, dummy_config_module: str) -> None:
    config = {
        "a": "hah",
        "b": [
            {
                "c": 1,
                "d": True,
                "e": "aha",
            },
        ],
        "c": f"inmanta://{dummy_config_module}/templates/test.j2",
    }

    config_text = yaml.safe_dump(config)
    config_file = pathlib.Path(project._test_project_dir) / "files/my-config-file.yml"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(config_text)

    project.compile(
        f"""
            import {dummy_config_module}
            import config

            conf = {dummy_config_module}::get_config()

            # Get a string config value
            assert_a = "hah"
            assert_a = config::get_config_value(conf, "a")
            assert_a = config::get_config_value_as_string(conf, "a")

            # Get a boolean config value from template
            assert_c = true
            assert_c = config::get_config_template_value_as_bool(conf, "c")
            assert_c = config::get_template_value_as_bool(conf, "c")
        """
    )


def test_multiple_configs(project: Project) -> None:
    model = """
        import config

        conf_a = {"a": "hah"}
        conf_b = {"a": "hbh"}

        # Get a string config value
        assert_a = "hah"
        assert_a = config::get_config_value(conf_a, "a")
        assert_a = config::get_config_value_as_string(conf_a, "a")

        # Get a string config value
        assert_b = "hbh"
        assert_b = config::get_config_value(conf_b, "a")
        assert_b = config::get_config_value_as_string(conf_b, "a")
    """

    project.compile(model, no_dedent=False)


def test_template_in_template(project: Project) -> None:
    templates = pathlib.Path(project._test_project_dir, "templates")
    templates.mkdir(parents=True, exist_ok=True)
    template_1 = templates / "1.j2"
    template_1.write_text("test1={{ test1 }}")
    template_2 = templates / "2.j2"
    template_2.write_text('{{ "/1.j2" | std.template(test1=test1)}}\ntest2={{ test2 }}')

    model = """
        import config

        assert_2 = config::get_template_value({"2": "template:///2.j2"}, "2", test1="1", test2="2")
        assert_2 = "test1=1\\ntest2=2"
    """
    project.compile(model)


def test_json(project: Project) -> None:
    """
    Test the usage of the json plugins
    """
    project.compile(
        """
        import config

        d = config::json_loads(s)
        d = {"a": "a", "b": [{"a": "a"}], "int": 0, "float": 1.0, "bool": true}
        s = config::json_dumps(d)
        s = '{"a": "a", "b": [{"a": "a"}], "int": 0, "float": 1.0, "bool": true}'
        """
    )

    # Entities can not be serialized
    with pytest.raises(inmanta.ast.ExternalException) as exc_info:
        project.compile(
            """
            import config

            entity A: end
            config::json_dumps(A())
            """
        )

    exc: inmanta.ast.ExternalException = exc_info.value
    assert re.match(
        r"@__config__::A [a-f0-9]+ is not JSON serializable",
        str(exc.__cause__),
    )
