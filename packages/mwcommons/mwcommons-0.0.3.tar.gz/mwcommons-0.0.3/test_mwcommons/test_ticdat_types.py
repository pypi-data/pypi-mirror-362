import unittest

from mwcommons.ticdat_types import (
    binary,
    float_number,
    integer_number,
    non_negative_float,
    non_negative_integer,
    positive_float,
    positive_integer,
    text,
)


class TestTicdatTypes(unittest.TestCase):
    def test_float_number(self):
        result = float_number()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": False,
            "min": -float("inf"),
            "inclusive_min": False,
            "max": float("inf"),
            "inclusive_max": False,
        }
        self.assertEqual(result, expected)

    def test_non_negative_float(self):
        result = non_negative_float()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": False,
            "min": 0.0,
            "inclusive_min": True,
            "max": float("inf"),
            "inclusive_max": False,
        }
        self.assertEqual(result, expected)

    def test_positive_float(self):
        result = positive_float()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": False,
            "min": 0.0,
            "inclusive_min": False,
            "max": float("inf"),
            "inclusive_max": False,
        }
        self.assertEqual(result, expected)

    def test_integer_number(self):
        result = integer_number()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": True,
            "min": -float("inf"),
            "inclusive_min": False,
            "max": float("inf"),
            "inclusive_max": False,
        }
        self.assertEqual(result, expected)

    def test_non_negative_integer(self):
        result = non_negative_integer()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": True,
            "min": 0,
            "inclusive_min": True,
            "max": float("inf"),
            "inclusive_max": False,
        }
        self.assertEqual(result, expected)

    def test_positive_integer(self):
        result = positive_integer()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": True,
            "min": 1,
            "inclusive_min": True,
            "max": float("inf"),
            "inclusive_max": True,
        }
        self.assertEqual(result, expected)

    def test_binary(self):
        result = binary()
        expected = {
            "number_allowed": True,
            "strings_allowed": (),
            "must_be_int": True,
            "min": 0,
            "inclusive_min": True,
            "max": 1,
            "inclusive_max": True,
        }
        self.assertEqual(result, expected)

    def test_text(self):
        result = text()
        expected = {"number_allowed": False, "strings_allowed": "*"}
        self.assertEqual(result, expected)

        # Test with custom strings_allowed
        custom_strings = ("A", "B", "C")
        result = text(strings_allowed=custom_strings)
        expected = {"number_allowed": False, "strings_allowed": custom_strings}
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
