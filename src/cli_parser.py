import sys
import logging
import argparse
from pathlib import Path


def parse_input():
    parser = argparse.ArgumentParser(description="Crawl files in your system.")
    subparsers = parser.add_subparsers(dest="command", help="Command to be executed")

    parse_scan_command(subparsers)
    parse_detect_command(subparsers)

    args = parser.parse_args()

    try:
        if not args.result_path.exists():
            raise FileNotFoundError(
                f"Provided path: `{args.result_path}` does not exist. Provide correct path."
            )
    except FileNotFoundError as e:
        logging.error(f"{e}")
        sys.exit(1)

    return args


def parse_scan_command(subparsers) -> None:
    scan_parser = subparsers.add_parser(
        "scan",
        help="Recursively finds all files in provided dirs. Collected metadata are saved as JSON. Example calls `scan . -rp .`, `scan -h` for more info",
    )
    scan_parser.add_argument(
        "scan_dirs",
        nargs="+",
        type=Path,
        help="Path to directories to scan. Provide at least one dir path.",
    )
    scan_parser.add_argument(
        "--result-path",
        "-rp",
        type=Path,
        default=Path.cwd(),
        help="Dir path to scan result. Result saved as `scan_output.json`. CWD used when not provided.",
    )
    scan_parser.add_argument(
        "--log-verbosity",
        "-lv",
        choices=["debug", "info"],
        default="info",
        help="Log verbosity level. Default level is INFO",
    )
    scan_parser.add_argument(
        "--log-output",
        "-lo",
        choices=["console", "logfile"],
        default="console",
        help="Log output. Default is console. Logfile name - `logfile.log`",
    )


def parse_detect_command(subparsers) -> None:
    detect_parser = subparsers.add_parser(
        "detect",
        help="""
        Generates diff between scan command result and same rescanned directories (listed in scan result). 
        Collected data are saved as JSON.
        Example call `detect DIR_PATH_TO_SCAN_RESULT -rp .`, `detect -h` for more info",
        """,
    )
    detect_parser.add_argument(
        "scan_result_path",
        type=Path,
        help="Dir path to scan result file. File must be named `scan_output.json`",
    )
    detect_parser.add_argument(
        "--result-path",
        "-rp",
        type=Path,
        default=Path.cwd(),
        help="Dir path to detect result. Result saved as `detect_output.json`. CWD used when not provided",
    )
    detect_parser.add_argument(
        "--log-verbosity",
        "-lv",
        choices=["debug", "info"],
        default="info",
        help="Log verbosity level. Default level is INFO.",
    )
    detect_parser.add_argument(
        "--log-output",
        "-lo",
        choices=["console", "logfile"],
        default="console",
        help="Log output. Default is console. Logfile name - `logfile.log`",
    )
