#!/usr/bin/env python3
import sys
from .core import convert_units

def main():
    if len(sys.argv) < 4:
        print("Usage:")
        print("  pconvert <value> <from_unit> <to_unit> [depth]")
        print("Example:")
        print("  pconvert 10 kilometer mile")
        print("  pconvert 10 kilometer mile 6")
        sys.exit(1)

    try:
        value = float(sys.argv[1])
        from_unit = sys.argv[2]
        to_unit = sys.argv[3]

        if len(sys.argv) >= 7:
            depth = int(sys.argv[4])
        else:
            depth = 7

        result = convert_units(value, from_unit, to_unit, depth)

        print(f"{value} {from_unit}(s) = {result:.6f} {to_unit}(s)")
        print(f"Recursive Depth Used: {depth}")

    except ValueError as ve:
        print(f"Error: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
