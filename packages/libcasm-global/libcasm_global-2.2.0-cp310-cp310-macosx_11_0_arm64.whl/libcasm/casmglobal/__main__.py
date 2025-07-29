import argparse
import sys
from typing import List, Any
from pathlib import Path
import libcasm.casmglobal


def main(argv: List[Any]) -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument("--cmakefiles", action='store_true', help="Print CASMcode_global project CMake module directory. Useful for setting CASMcode_global_ROOT in CMake.")
    parser.add_argument("--prefix", action='store_true', help="Print CASM package installation prefix. Useful for setting CMAKE_PREFIX_PATH in CMake.")

    args = parser.parse_args(args=argv[1:])

    if not argv[1:]:
        parser.print_help()
        return

    prefix = Path(libcasm.casmglobal.__file__).parent.parent

    if args.cmakefiles:
        print(prefix / "share/CASMcode_global/cmake")

    if args.prefix:
        print(prefix)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
