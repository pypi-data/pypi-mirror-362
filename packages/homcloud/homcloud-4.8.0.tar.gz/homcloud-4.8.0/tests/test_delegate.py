from homcloud.delegate import forwardable


@forwardable
class ClassA:
    def __init__(self) -> None:
        self.x = "foobar"
        self.y = "Baz"

    __delegator_definitions__ = {"x": ["capitalize", "upper"], "y": "lower"}


def test_forwardable():
    a = ClassA()
    assert a.capitalize() == "Foobar"
    assert a.upper() == "FOOBAR"
    assert a.lower() == "baz"
