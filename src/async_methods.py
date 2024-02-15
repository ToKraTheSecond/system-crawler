import asyncio

from pathlib import Path


async def async_scan(dirs: list[Path], result_path: Path, scan_method) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, scan_method, dirs, result_path)


async def async_detect(
    scan_result_path: Path, result_path: Path, detect_method
) -> None:
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, detect_method, scan_result_path, result_path)
