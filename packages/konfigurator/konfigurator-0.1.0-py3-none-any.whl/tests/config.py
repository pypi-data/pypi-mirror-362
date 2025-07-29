"""
Config file for testing
"""
import os

# from .test_instantiation import MyTestClass

_work_dir = "tests/work_dir"
experiment_dir = os.path.join(_work_dir, "experiment")

class_config_1 = dict(
    type="tests.test_utils.MyTestClass",
    name="test_instance_1",
)
