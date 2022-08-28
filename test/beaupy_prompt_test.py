from ward import test, raises
from beaupy import prompt, console, ConversionError, ValidationError
import readchar
from unittest import mock

from beaupy.beaupy import Config


@test("Empty prompt with immediately pressing confirm", tags=["v1", "prompt"])
def _():
    steps = iter([readchar.key.ENTER])

    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("")

    console.print.assert_called_once_with("\n> ")
    assert res == ""


@test("Empty prompt typing `jozo` without validation and type and pressing confirm", tags=["v1", "prompt"])
def _():
    steps = iter(["j", "o", "z", "o", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("")

    assert console.print.call_args_list == [
        mock.call("\n> "),
        mock.call("\n> j"),
        mock.call("\n> jo"),
        mock.call("\n> joz"),
        mock.call("\n> jozo"),
    ]
    assert res == "jozo"


@test("Empty prompt typing `jozo` as secure input without validation and type and pressing confirm", tags=["v1", "prompt"])
def _():
    steps = iter(["j", "o", "z", "o", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("", secure=True)

    assert console.print.call_args_list == [
        mock.call("\n> "),
        mock.call("\n> *"),
        mock.call("\n> **"),
        mock.call("\n> ***"),
        mock.call("\n> ****"),
    ]
    assert res == "jozo"


@test("Empty prompt typing `True` as secure input with bool as type", tags=["v1", "prompt"])
def _():
    steps = iter(["T", "r", "u", "e", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("", secure=True, target_type=bool)

    assert console.print.call_args_list == [
        mock.call("\n> "),
        mock.call("\n> *"),
        mock.call("\n> **"),
        mock.call("\n> ***"),
        mock.call("\n> ****"),
    ]
    assert res is True


@test("Empty prompt typing `12` as secure input with float as type", tags=["v1", "prompt"])
def _():
    steps = iter(["1", "2", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("", secure=True, target_type=float)

    assert console.print.call_args_list == [mock.call("\n> "), mock.call("\n> *"), mock.call("\n> **")]
    assert isinstance(res, float)
    assert res == 12.0


@test("`Ask an actual question goddammit` as a prompt typing `No` and validating it is `No`", tags=["v1", "prompt"])
def _():
    steps = iter(["N", "o", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt("Ask an actual question goddammit", validator=lambda val: val == "No")

    assert console.print.call_args_list == [
        mock.call("Ask an actual question goddammit\n> "),
        mock.call("Ask an actual question goddammit\n> N"),
        mock.call("Ask an actual question goddammit\n> No"),
    ]
    assert isinstance(res, str)
    assert res == "No"


@test("Empty prompt typing `12` as secure input with bool as type raising ConversionError", tags=["v1", "prompt"])
def _():
    steps = iter(["1", "2", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()

    with raises(ConversionError):
        prompt("", secure=True, target_type=bool)
        assert console.print.call_args_list == [mock.call("\n> "), mock.call("\n> *"), mock.call("\n> **")]


@test("Empty prompt typing `12` as secure input with bool as type raising ConversionError", tags=["v1", "prompt"])
def _():
    steps = iter(["1", "2", readchar.key.ENTER])
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()

    with raises(ValidationError):
        prompt("", secure=True, target_type=float, validator=lambda val: val > 20)
        assert console.print.call_args_list == [mock.call("\n> "), mock.call("\n> *"), mock.call("\n> **")]


@test("Prompt with typing `J`, then deleting it and typing `No`", tags=["v1", "prompt"])
def _():
    steps = iter(["J", readchar.key.BACKSPACE, "N", "o", readchar.key.ENTER])

    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    res = prompt(prompt="Try test")
    assert res == "No"


@test("Prompt with interrupt and raise on keyboard iterrupt as False", tags=["v1", "prompt"])
def _():
    steps = iter([readchar.key.CTRL_C])
    Config.raise_on_interrupt = False
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()
    ret = prompt(prompt="Try test")

    assert ret is None


@test("Prompt with interrupt and raise on keyboard iterrupt as True", tags=["v1", "prompt"])
def _():
    steps = iter([readchar.key.CTRL_C])
    Config.raise_on_interrupt = True
    readchar.readkey = lambda: next(steps)
    console.print = mock.MagicMock()

    with raises(KeyboardInterrupt):
        prompt(prompt="Try test")
