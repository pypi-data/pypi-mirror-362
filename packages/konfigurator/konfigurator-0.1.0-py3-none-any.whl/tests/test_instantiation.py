from konfigurator import class_from_path, get_class_path, instantiate_object_from_config


class MyTestClass:
    def __init__(self, name: str, func=None) -> None:
        self._name = name
        self._func = func

    @property
    def name(self) -> str:
        return self._name


def test_my_test_class():
    class_name = get_class_path(MyTestClass)
    assert class_name == "test_instantiation.MyTestClass"


def test_class_from_path():
    class_name = get_class_path(MyTestClass)
    cls = class_from_path(class_name)
    assert cls is MyTestClass


def test_instantiate_object_from_config():
    def non_pickable():
        yield from range(10)

    config = {
        "type": "test_instantiation.MyTestClass",
        "name": "test_instance",
        "func": non_pickable(),
    }
    instance = instantiate_object_from_config(config)
    assert instance.__class__ is MyTestClass
    assert instance.name == "test_instance"
