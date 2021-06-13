from typing import Optional, Sequence
import argparse
from pathlib import Path
from db import init_db
from get import parse_all_pages
from utils import write_json


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-p",
        "--json-path",
        dest="json_path",
        default=Path("all_popular_quotes.json"),
        type=Path,
        help="path to output json file",
    )
    parser.add_argument(
        "-t",
        "--tinydb-path",
        dest="tinydb_path",
        default=None,
        type=Path,
        help="path to tinydb file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help="verbosity",
    )

    args = parser.parse_args(argv)

    quotes = parse_all_pages(verbose=args.verbose)
    write_json(args.json_path, quotes)
    if args.tinydb_path:
        init_db(args.tinydb_path, args.json_path)


if __name__ == "__main__":
    main()
