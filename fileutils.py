#!/usr/bin/python
"""
Some file utilities
"""


from __future__ import annotations


def mkdir(directory):
    import os

    if not os.path.isdir(directory):
        os.mkdir(directory)


def create_dir(directory):
    mkdir(directory)


def nonrecursive_find(inspec):
    import glob

    matches = glob.glob(inspec)
    return matches


def recursive_find(inspec):
    import fnmatch
    import os

    matches = []
    head, tail = os.path.split(inspec)
    if len(head) == 0:
        head = "."

    for root, dirnames, filenames in os.walk(head):
        for filename in fnmatch.filter(filenames, tail):
            matches.append(os.path.join(root, filename))

    return matches


def find_files(inspec, recursive=False):
    if recursive:
        files = recursive_find(inspec)
    else:
        files = nonrecursive_find(inspec)
    return files


def call_cmd(cmd, add_dot=True):
    import os

    if add_dot and os.name != "nt":
        cmd = "./" + cmd
    print(cmd)
    os.system(cmd)


def get_extension(filename):
    import os

    filename, extension = os.path.splitext(filename)
    return extension


if __name__ == "__main__":
    import argparse

    try:
        import timing  # optional

        assert timing  # silence warnings
    except ImportError:
        pass

    parser = argparse.ArgumentParser(description="List files.")
    parser.add_argument("-i", "--inspec", default="*", help="Input file spec.")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse directories."
    )
    args = parser.parse_args()
    print(args)

    if args.recursive:
        print("Recursive:")
    else:
        print("Non-recursive:")

    files = find_files(args.inspec, args.recursive)
    print(len(files), "files found")

# End of file
