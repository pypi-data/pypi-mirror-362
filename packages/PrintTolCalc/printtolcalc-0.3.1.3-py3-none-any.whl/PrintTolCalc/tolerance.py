# SPDX-License-Identifier: LicenseRef-OQL-1.2


def calculate_tolerance(expected, measured):
    tolerances = {}
    for axis, e, m in zip(["X", "Y", "Z"], expected, measured):
        if e == 0:
            raise ValueError(f"Expected value for {axis}-axis cannot be zero.")
        if e < 0:
            raise ValueError(f"Expected value for {axis}-axis cannot be negative.")
        signed = ((m - e) / e) * 100
        absolute = abs(signed)
        tolerances[axis] = {"signed": signed, "absolute": absolute}
    return tolerances
