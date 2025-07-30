# config module

This module contains some helper plugins to get value from a config file in the context of an inmanta model.  

The config itself and the logic to gather it should still be included in the modules that make use of it.  This module's main function is to make it easier to handle those and to propose a consistent config handling mechanism across different modules.

## Features

- Use a YAML file and extract values from it
- Use Jinja file as template

## Example of usage

### In the plugin

```py
import typing

import pydantic

import inmanta.plugins
import inmanta_plugins.config
import inmanta_plugins.config.abc
import inmanta_plugins.config.const

CONFIG_PATH = "inmanta:///files/my-config-file.yml"


class ConfigElem(pydantic.BaseModel):
    c: int
    d: bool
    e: str


class Config(inmanta_plugins.config.abc.ConfigABC):
    a: str
    b: typing.Sequence[ConfigElem]
    c: typing.Union[inmanta_plugins.config.const.InmantaPath, bool]

    @classmethod
    def raw_config_path(cls) -> str:
        return CONFIG_PATH


@inmanta.plugins.plugin
def get_config() -> "dict":
    return Config.load().as_dict()

```

### In the config file

```yaml
a: hah
b:
- c: 1
  d: true
  e: aha
c: inmanta:///templates/test.j2
```

### In the Jinja file

```jinja
True
```

### In the model

```
import config

conf = get_config()

# Get a string config value
config::get_config_value(conf, "a")
config::get_config_value_as_string(conf, "a")

# Get an integer config value
config::get_config_value(conf, "b[c=1].c")
config::get_config_value_as_int(conf, "b[c=1].c")

# Get an boolean config value
config::get_config_value(conf, "b[c=1].d")
config::get_config_value_as_bool(conf, "b[c=1].d")

# Get a config value from template
config::get_config_template_value_as_bool(conf, "c")
config::get_template_value_as_bool(conf, "c")
```

```{toctree}
:maxdepth: 1
autodoc.rst
CHANGELOG.md
```
