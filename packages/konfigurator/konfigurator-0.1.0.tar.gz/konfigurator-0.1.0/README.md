![Tests](https://github.com/isealab/konfigurator/actions/workflows/test.yml/badge.svg)

# konfigurator

**konfigurator** is a lightweight Python configuration management utility that allows you to define, override, and instantiate configuration dictionaries and Python classes from simple config files or command-line arguments.

Further, it allows you to instantiate objects from classes using import paths. In this way, *no global registry or any disclosure* of your private code is needed.

The instantiation via import path is inspired by https://github.com/Farama-Foundation/HighwayEnv

## Features

- Load Python-based configuration files as dictionaries.
- Override configuration parameters via command-line.
- Instantiate Python classes from config dictionaries using import paths.

## Installation
`cd` into repository and run
```bash
pip install .
````

To install in developer mode (with `pre-commit` and `pytest`) run
```bash
pip install -e .[dev,test]
```

## Usage

1. Load a configuration file

    Your configuration file is a pure python file (e.g., config.py) should define a dictionary named config:
    ```python
    # config.py
    work_dir = "/tmp/my_work_dir"
    class_config_1: {
        "type": "my_module.MyClass",
        "name": "default_name"
    }
    ```
    You will be able to instantiate an object from the configuration `class_config_1` (see ).

    Load this configuration in Python:
    ```python
    from konfigurator import load_config

    config = load_config(config_path="config.py")
    ```

2. Override from command-line and save result

    You can override nested config values via CLI and save the modified config to disk, e.g.:
    ```bash
    python script.py \
    --config config.py \
    --override experiment_dir=/tmp/experiment \
    --override class_config_1.name=overridden_name \
    --override class_config_1.type=5.0
    ```
    Currently, floats, ints, and booleans are converted into their respective type. Strings and other types remain strings.

3. Instantiate classes from config

    Use the `instantiate_class_from_config` to build objects dynamically (IMPORTANT: the value for the key `type` defines the import path):
    ```python
    from konfigurator import instantiate_object_from_config

    class_config_1: {
        "type": "my_module.MyClass",
        "name": "default_name"
    }

    my_obj = instantiate_object_from_config(class_config_1)
    ```
