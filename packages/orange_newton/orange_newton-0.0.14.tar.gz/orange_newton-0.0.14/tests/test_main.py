import pytest

from orange_newton.main import Calc, Person, add, hello, minus


def test_hello(capfd: pytest.CaptureFixture):
    expected = "Hello, Python\n"
    hello()
    out, err = capfd.readouterr()
    assert out == expected
    assert err == ""


def test_add01():
    expected = 5
    assert Calc(3, 2).add() == expected


def test_add02():
    expected = 5
    assert Calc(-5, 10).add() == expected


def test_minus01():
    expected = 3
    assert Calc(5, 2).minus() == expected


def test_minus02():
    expected = 3
    assert Calc(-3, -6).minus() == expected


def test_multiply01():
    expected = 8
    assert Calc(4, 2).multiply() == expected


def test_multiply02():
    expected = -8
    assert Calc(-4, 2).multiply() == expected


def test_divide01():
    expected = 4
    assert Calc(8, 2).divide() == expected


def test_divide02():
    expected = -4
    assert Calc(-8, 2).divide() == expected


def test_add():
    expected = 3
    assert add(1, 2) == expected


def test_minus():
    expected = 3
    assert minus(5, 2) == expected


def test_person01():
    expected = "Bob"
    assert Person(expected).get_name() == expected


def test_person02():
    name = "Tom"
    expected = "My name is " + name
    assert Person(name).say_name() == expected
