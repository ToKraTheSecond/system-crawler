import os
import logging
from pathlib import Path


def get_paths(dir_path: Path) -> set[Path]:
    """
    Recursively finds all file paths for given dir path
    """
    return set(dir_path.rglob("*.*"))


def get_file_metadata(file_path: Path) -> dict:
    logging.debug(f"Getting metadata for file {file_path}")
    try:
        file_info = os.stat(file_path)
        return {
            "file_size": file_info.st_size,
            "creation_time": file_info.st_ctime,
            "modification_time": file_info.st_mtime,
        }
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except PermissionError:
        logging.error(f"Permission error for {file_path}")
    except Exception as e:
        logging.error(f"Error during getting metadata for {file_path}: {e}")

    return {
        "file_size": None,
        "creation_time": None,
        "modification_time": None,
    }


def compare_metadata(scan_metadata: dict, detect_metadata: dict) -> dict[str, list]:
    scan_files = set(scan_metadata.keys())
    detect_files = set(detect_metadata.keys())

    added_files = detect_files.difference(scan_files)
    removed_files = scan_files.difference(detect_files)
    present_files = detect_files & scan_files
    unchanged_files = []
    changed_files_by_size = []

    for file in present_files:
        logging.debug(f"Comparing metadata for file {file}")
        is_size_same = (
            scan_metadata[file]["file_size"] == detect_metadata[file]["file_size"]
        )
        if is_size_same:
            unchanged_files.append(file)
        else:
            changed_files_by_size.append(file)

    return {
        "added_files": list(added_files),
        "removed_files": list(removed_files),
        "changed_files_by_size": changed_files_by_size,
        "unchanged_files": unchanged_files,
    }
