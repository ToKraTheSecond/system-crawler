import sys
import logging
import json

from pathlib import Path
from abc import ABC, abstractmethod


class FileWrite(ABC):
    @abstractmethod
    def save(self, data: dict, file_path: Path):
        pass


class FileRead(ABC):
    @abstractmethod
    def read(self, file_path: Path):
        pass


class JsonFileWrite(FileWrite):
    def save(self, data: dict, file_path: Path) -> None:
        with open(str(file_path), "w") as f:
            json.dump(data, f, indent=2)
        logging.info(f"File `{file_path}` saved")


class JsonFileRead(FileRead):
    def read(self, file_path: Path):
        try:
            with open(str(file_path), "r") as f:
                return json.load(f)
        except FileNotFoundError:
            logging.error(
                f"File: `{file_path}` not found. Please provide correct path."
            )
            sys.exit(1)
