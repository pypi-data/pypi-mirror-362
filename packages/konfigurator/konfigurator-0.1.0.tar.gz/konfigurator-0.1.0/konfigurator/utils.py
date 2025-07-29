import importlib
import importlib.util
import os
import sys
from importlib.machinery import ModuleSpec
from typing import Callable, Optional


def get_class_path(cls: Callable) -> str:
    """
    Returns the full path of a class as a string.

    Copied from https://github.com/Farama-Foundation/HighwayEnv
    """
    return cls.__module__ + "." + cls.__qualname__


def class_from_path(path: str) -> Callable:
    """
    Returns a class object from its full path.
    The path should be in the format 'module.ClassName'.

    Copied from https://github.com/Farama-Foundation/HighwayEnv
    """
    module_name, class_name = path.rsplit(".", 1)
    class_object = getattr(importlib.import_module(module_name), class_name)
    return class_object


def instantiate_object_from_config(config: dict) -> Callable:
    """
    Instantiates a class from a configuration dictionary.
    The dictionary must contain a 'type' key with the full class path.
    """
    assert "type" in config, "Config must contain 'type' key"
    class_path = config["type"]
    params = {k: v for k, v in config.items() if not k == "type"}
    class_object = class_from_path(class_path)
    return class_object(**params)


def load_config(*, config_path: str) -> dict:
    """
    Load a Python configuration file and extract its variables into a dictionary.
    Variables that start with an underscore, callable objects, and modules are filtered out.
    """
    config_path = os.path.abspath(config_path)
    spec = importlib.util.spec_from_file_location("user_config", config_path)
    assert isinstance(spec, ModuleSpec), "Failed to load module spec"

    config = importlib.util.module_from_spec(spec)
    sys.modules["user_config"] = config
    spec.loader.exec_module(config)

    # Extract variables: filter out built-ins and modules
    config_dict = {
        key: value
        for key, value in vars(config).items()
        if not key.startswith("_")
        and not callable(value)
        and not isinstance(value, type(sys))
    }
    return config_dict


def update_config_with_overrides(
    *, config: dict, overrides: Optional[list[str]]
) -> dict:
    """
    Update the configuration dictionary with command line overrides.
    Each override should be in the format 'key=value'.
    e.g. "--override port=9090 --override config.batch_size=32"
    """
    if overrides:
        for item in overrides:
            key, value = item.split("=", 1)
            set_nested(config, key, value)
    return config


def set_nested(config, var_path, value):
    """
    Set a nested value in config given a dotted path (e.g., my_dict.name).
    """
    keys = var_path.split(".")
    obj = config
    for key in keys[:-1]:
        obj = getattr(obj, key) if hasattr(obj, key) else obj[key]

    if value.lower() == "true":
        value = True
    elif value.lower() == "false":
        value = False
    else:
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass
    obj[keys[-1]] = value
