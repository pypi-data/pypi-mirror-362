
from argparse import ArgumentParser
from pathlib import Path

from .diff import diffToJSONFile, readDifferencesJSONFile
from .io import readBytesFromPath, writeBytesToPath
from .patch import patchFromDifferences


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('-a', type=Path)
    parser.add_argument('-b', type=Path)
    parser.add_argument('-json', type=Path)

    parser.add_argument('--diff', action='store_true')
    parser.add_argument('--patch', action='store_true')

    args = parser.parse_args()

    if args.diff:
        aData = readBytesFromPath(args.a)
        bData = readBytesFromPath(args.b)
        diffToJSONFile(aData, bData, args.json)

    elif args.patch:
        aData = bytearray(readBytesFromPath(args.a))
        differences = readDifferencesJSONFile(args.json)
        patched = patchFromDifferences(aData, differences)
        writeBytesToPath(args.b, patched)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
