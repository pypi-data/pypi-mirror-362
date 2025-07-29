# SPDX-License-Identifier: LicenseRef-OQL-1.2

import argparse
from .tolerance import calculate_tolerance

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("PrintTolCalc")
except PackageNotFoundError:
    __version__ = "STANDALONE"


def prompt_for_dimensions(label):
    print(f"\nEnter {label} dimensions (in mm):")
    x = float(input(" X: "))
    y = float(input(" Y: "))
    z = float(input(" Z: "))
    return (x, y, z)


def main():
    parser = argparse.ArgumentParser(
        description=f"PrintTolCalc CLI {__version__} - Calculate 3D print dimensional tolerance.",
        epilog="""
Examples:
  PrintTolCalc
    → Interactive mode, will prompt for expected/measured dimensions.

  PrintTolCalc --expected 20 20 20 --measured 19.99 19.95 20.10
    → Command-line mode, pass dimensions directly.

All dimensions must be in millimeters (mm).
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", action="version", version=f"PrintTolCalc {__version__}"
    )
    parser.add_argument(
        "--expected",
        type=float,
        nargs=3,
        metavar=("X", "Y", "Z"),
        help="Expected dimensions in mm (e.g. --expected 20 20 20)",
    )
    parser.add_argument(
        "--measured",
        type=float,
        nargs=3,
        metavar=("X", "Y", "Z"),
        help="Measured dimensions in mm (e.g. --measured 19.99 19.95 20.10)",
    )

    args = parser.parse_args()

    expected = args.expected if args.expected else prompt_for_dimensions("expected")
    measured = args.measured if args.measured else prompt_for_dimensions("measured")

    tolerances = calculate_tolerance(expected, measured)

    print("\n3D Print Tolerance Report:")
    print(f"Ideal X dimension (mm): {expected[0]:.2f}")
    print(f"Ideal Y dimension (mm): {expected[1]:.2f}")
    print(f"Ideal Z dimension (mm): {expected[2]:.2f}")
    print(f"Measured X dimension (mm): {measured[0]:.2f}")
    print(f"Measured Y dimension (mm): {measured[1]:.2f}")
    print(f"Measured Z dimension (mm): {measured[2]:.2f}")
    print("\nTolerance Results:")
    for axis in ["X", "Y", "Z"]:
        signed = tolerances[axis]["signed"]
        absolute = tolerances[axis]["absolute"]
        sign_prefix = "+" if signed > 0 else ""
        print(
            f"{axis}-axis: Signed = {sign_prefix}{signed:.3f}%, Absolute = {absolute:.3f}%"
        )


if __name__ == "__main__":
    main()
