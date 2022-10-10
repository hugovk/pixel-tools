#!/usr/bin/env python
"""
Print the factors of an integer or a number of files

Usage: factors.py INTEGER
Usage: factors.py FILESPEC
Usage: factors.py [*.jpg]
"""
from __future__ import annotations

import sys
from functools import reduce


def factors(n):
    return reduce(
        list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0)
    )


def get_middleish_factor(n):
    # Grab a middle-ish factor
    factors_set = factors(n)
    factors_list = list(sorted(factors_set))
    return factors_list[int(len(factors_list) / 2) - 1]


if __name__ == "__main__":
    inspec = None
    if len(sys.argv) < 2:
        inspec = "*.jpg"
    elif str.isdigit(sys.argv[1]):
        numerator = int(sys.argv[1])
    else:
        inspec = sys.argv[1]

    if inspec:
        import glob

        infiles = glob.glob(inspec)
        numerator = len(infiles)

    my_factors = factors(numerator)
    my_factors.sort()
    for f in my_factors:
        print(numerator, "=", f, "*", numerator / f)

    print("Middle-ish factor:", get_middleish_factor(numerator))

# End of file
