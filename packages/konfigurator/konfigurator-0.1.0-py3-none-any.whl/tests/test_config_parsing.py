import json
import os
import subprocess
import tempfile

from konfigurator import load_config

this_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(this_dir, "config.py")
script_path = os.path.join(this_dir, "script.py")


def test_load_config():
    config = load_config(config_path=config_path)
    assert isinstance(config, dict), "Config should be a dictionary"
    assert "experiment_dir" in config, "Config should contain 'experiment_dir'"
    assert "class_config_1" in config, "Config should contain 'class_config_'"
    assert "_test_class_obj" not in config, "Config should contain '_test_class_obj'"


def test_override_from_cli():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as temp_file:
        temp_file_path = temp_file.name

        subprocess.run(
            [
                "python",
                script_path,
                "--config",
                config_path,
                "--override",
                "experiment_dir=/tmp/experiment",
                "--override",
                "class_config_1.name=overridden_name",
                "--override",
                "class_config_1.type=5.",
                "--save_to",
                temp_file_path,
            ],
            check=True,
        )

        # Load the resulting config file
        with open(temp_file_path, "r") as f:
            config = json.load(f)

        assert (
            config["experiment_dir"] == "/tmp/experiment"
        ), "Experiment dir should be overridden"
        assert (
            config["class_config_1"]["name"] == "overridden_name"
        ), "Class config name should be overridden"
        assert (
            config["class_config_1"]["type"] == 5.0
        ), "Config type should be overridden to 5.0"
