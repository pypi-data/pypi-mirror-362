import json
import sys
from math import floor
from multiprocessing import cpu_count
from pathlib import Path
from loguru import logger

__all__ = [
    "config_path",
    "dbase_config_file",
    "segmentation_config_file",
    "read_segmentation_config",
    "read_dbase_config",
    "logger_setup",
    "set_threads_per_process",
]

config_path = Path(__file__).parent.resolve()
dbase_config_file = config_path / "dbase.json"
segmentation_config_file = config_path / "segmentation_models.json"


def read_segmentation_config():
    if not segmentation_config_file.exists():
        logger.error(
            f"Segmentation config file {segmentation_config_file} does not exist. Add some segmentation models with mircat-v2 models add"
        )
        sys.exit(1)
    with segmentation_config_file.open() as f:
        return json.load(f)


def read_dbase_config():
    if not dbase_config_file.exists():
        logger.error(
            f"DBase config file {dbase_config_file} does not exist. Please check path or use mircat-v2 dbase create"
        )
        sys.exit(1)
    with dbase_config_file.open() as f:
        return json.load(f)


def logger_setup(verbose: bool, quiet: bool) -> None:
    """Set up logger for mircat-v2
    :param verbose: be verbose in the output by adding debug to stdout
    :param quiet: be quiet in the output by only showing successes and errors - no warnings or info.
    """
    logger.remove()
    # Regular
    stdout_fmt = "<green>{time: DD-MM-YYYY -> HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>"
    stderr_fmt = "<red>{time: DD-MM-YYYY -> HH:mm:ss}</red> | <level>{level}</level> | <level>{message}</level>"
    if quiet:
        # Only show success messages and error messages
        logger.add(
            sys.stdout,
            format=stdout_fmt,
            level="SUCCESS",
            filter=lambda record: record["level"].no <= 25,
            enqueue=True,
        )
        logger.add(sys.stderr, format=stderr_fmt, level="ERROR", enqueue=True)
    elif verbose:
        # Include debugging output
        logger.add(
            sys.stdout,
            format=stdout_fmt,
            level="DEBUG",
            filter=lambda record: record["level"].no <= 25,
            enqueue=True,
        )
        logger.add(
            sys.stderr,
            format=stderr_fmt,
            level="WARNING",
            enqueue=True,
        )
    else:
        # Show everything above INFO
        logger.add(
            sys.stdout,
            format=stdout_fmt,
            level="INFO",
            filter=lambda record: record["level"].no <= 25,
            enqueue=True,
        )
        logger.add(
            sys.stderr,
            format=stderr_fmt,
            level="WARNING",
            enqueue=True,
        )


def set_threads_per_process(args):
    # Do some thread matching
    total_threads = cpu_count()
    required_threads = args.n_processes * args.threads_per_process
    logger.debug(
        f"Total threads on machine: {total_threads}. Requested threads for segmentation: {required_threads}"
    )
    if total_threads < required_threads:
        args.threads_per_process = floor(total_threads / args.n_processes)
        logger.warning(
            "Desired threads (n_processes * threads_per_process) > total threads on device ({}>{}). Limiting threads per worker to {}. If performance drops, consider reducing the number of workers and upping threads to match.",
            required_threads,
            total_threads,
            args.threads_per_process,
        )
