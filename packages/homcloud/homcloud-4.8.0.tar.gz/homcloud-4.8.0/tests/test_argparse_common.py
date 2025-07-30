import pytest

from homcloud.argparse_common import parse_range, parse_color


def test_parse_range():
    assert (-2.0, 5.0) == parse_range("-2:5")
    assert (1.2, 2.4) == parse_range("1.2:2.4")
    assert (-2.0, 5.0) == parse_range("[-2:5.0]")
    with pytest.raises(ValueError):
        parse_range("[-2:5")
    with pytest.raises(ValueError):
        parse_range(" [-2.0:5]")


def test_parse_color():
    assert parse_color("#ff00ff") == (255, 0, 255)
    assert parse_color("#000000") == (0, 0, 0)
    with pytest.raises(ValueError):
        parse_color("ff00ff")
    with pytest.raises(ValueError):
        parse_color("#fff")
