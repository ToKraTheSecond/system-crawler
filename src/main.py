import asyncio
from pathlib import Path

from logger import setup_logger
from cli_parser import parse_input
from crawler import get_paths, get_file_metadata, compare_metadata
from data_io import JsonFileWrite, JsonFileRead
from async_methods import async_scan, async_detect

json_write = JsonFileWrite()
json_read = JsonFileRead()

RUN_ASYNC = False
SCAN_OUTPUT_NAME = "scan_output.json"
DETECT_OUTPUT_NAME = "detect_output.json"
LOGFILE_NAME = "logfile.log"


def scan(dirs: list[Path], result_path: Path) -> None:
    """
    Scans for all files in given dir paths and all their subdirectories.
    Generates metadata about the files and saves it to result file with given `result_path`.
    """
    paths = {path for dir in dirs for path in get_paths(dir)}

    metadata: dict[str, dict | list] = {}
    metadata["metadata"] = {str(path): get_file_metadata(path) for path in paths}
    metadata["scanned_dirs"] = [str(dir) for dir in dirs]

    json_write.save(metadata, result_path / SCAN_OUTPUT_NAME)


def detect(scan_result_path: Path, result_path: Path) -> None:
    """
    Detects changes in files -> current state vs scan result state.
    Saves generated data it to result file with given `result_path`.
    """
    scan_result = json_read.read(scan_result_path / SCAN_OUTPUT_NAME)

    scanned_dirs = scan_result["scanned_dirs"]
    scan_metadata = scan_result["metadata"]

    paths = {path for dir in scanned_dirs for path in get_paths(Path(dir))}
    detect_metadata = {str(path): get_file_metadata(path) for path in paths}

    result = compare_metadata(scan_metadata, detect_metadata)
    json_write.save(result, result_path / DETECT_OUTPUT_NAME)


if __name__ == "__main__":
    args = parse_input()
    setup_logger(args, logfile_name=LOGFILE_NAME)

    if RUN_ASYNC:
        if args.command == "scan":
            asyncio.run(async_scan(args.scan_dirs, args.result_path, scan))
        elif args.command == "detect":
            asyncio.run(async_detect(args.scan_result_path, args.result_path, detect))
    else:
        if args.command == "scan":
            scan(args.scan_dirs, args.result_path)
        elif args.command == "detect":
            detect(args.scan_result_path, args.result_path)
