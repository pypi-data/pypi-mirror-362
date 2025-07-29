# SPDX-License-Identifier: LicenseRef-OQL-1.2

import pytest
from PrintTolCalc.tolerance import calculate_tolerance


def test_perfect_match():
    expected = (20, 20, 20)
    measured = (20, 20, 20)
    result = calculate_tolerance(expected, measured)
    for axis in ["X", "Y", "Z"]:
        assert result[axis]["signed"] == pytest.approx(0.0)
        assert result[axis]["absolute"] == pytest.approx(0.0)


def test_negative_deviation():
    expected = (20, 20, 20)
    measured = (19, 19, 19)
    result = calculate_tolerance(expected, measured)
    for axis in ["X", "Y", "Z"]:
        assert result[axis]["signed"] == pytest.approx(-5.0)
        assert result[axis]["absolute"] == pytest.approx(5.0)


def test_positive_deviation():
    expected = (10, 10, 10)
    measured = (10.5, 11, 12)
    result = calculate_tolerance(expected, measured)
    assert result["X"]["signed"] == pytest.approx(5.0)
    assert result["Y"]["signed"] == pytest.approx(10.0)
    assert result["Z"]["signed"] == pytest.approx(20.0)


def test_mixed_deviation():
    expected = (10, 20, 30)
    measured = (9.5, 20, 31.5)
    result = calculate_tolerance(expected, measured)
    assert result["X"]["signed"] == pytest.approx(-5.0)
    assert result["Y"]["signed"] == pytest.approx(0.0)
    assert result["Z"]["signed"] == pytest.approx(5.0)


@pytest.mark.parametrize(
    "index,axis,bad_value,expected_message",
    [
        (0, "X", 0, "Expected value for X-axis cannot be zero."),
        (1, "Y", 0, "Expected value for Y-axis cannot be zero."),
        (2, "Z", 0, "Expected value for Z-axis cannot be zero."),
        (0, "X", -1, "Expected value for X-axis cannot be negative."),
        (1, "Y", -1, "Expected value for Y-axis cannot be negative."),
        (2, "Z", -1, "Expected value for Z-axis cannot be negative."),
    ],
)
def test_invalid_expected_values(index, axis, bad_value, expected_message):
    expected = [20, 20, 20]
    measured = [20, 20, 20]
    expected[index] = bad_value

    with pytest.raises(ValueError, match=expected_message):
        calculate_tolerance(tuple(expected), tuple(measured))
