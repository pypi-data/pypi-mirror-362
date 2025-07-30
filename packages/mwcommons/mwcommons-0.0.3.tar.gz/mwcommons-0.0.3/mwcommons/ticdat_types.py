"""
The types to be used in the data schema built with ticdat.
Remark: use only aliases that match perfectly your needs, otherwise set datatype explicitly
"""


def float_number(
    min: float = -float("inf"),
    inclusive_min: bool = False,
    max: float = float("inf"),
    inclusive_max: bool = False,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": False,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def non_negative_float(
    min: float = 0.0,
    inclusive_min: bool = True,
    max: float = float("inf"),
    inclusive_max: bool = False,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": False,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def positive_float(
    min: float = 0.0,
    inclusive_min: bool = False,
    max: float = float("inf"),
    inclusive_max: bool = False,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": False,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def integer_number(
    min: int = -float("inf"),
    inclusive_min: bool = False,
    max: float = float("inf"),
    inclusive_max: bool = False,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": True,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def non_negative_integer(
    min: int = 0,
    inclusive_min: bool = True,
    max: float = float("inf"),
    inclusive_max: bool = False,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": True,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def positive_integer(
    min: int = 1,
    inclusive_min: bool = True,
    max: float = float("inf"),
    inclusive_max: bool = True,
):
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": True,
        "min": min,
        "inclusive_min": inclusive_min,
        "max": max,
        "inclusive_max": inclusive_max,
    }


def binary():
    return {
        "number_allowed": True,
        "strings_allowed": (),
        "must_be_int": True,
        "min": 0,
        "inclusive_min": True,
        "max": 1,
        "inclusive_max": True,
    }


def text(strings_allowed: tuple | str = "*"):
    return {"number_allowed": False, "strings_allowed": strings_allowed}
