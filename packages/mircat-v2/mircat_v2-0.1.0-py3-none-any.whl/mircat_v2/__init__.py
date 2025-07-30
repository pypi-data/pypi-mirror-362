import os

os.environ["nnUNet_raw"] = ""
os.environ["nnUNet_preprocessed"] = ""
os.environ["nnUNet_results"] = ""

import argparse

from loguru import logger

from mircat_v2.configs import logger_setup
from mircat_v2.dicom_conversion import (
    convert_dicoms_to_nifti,
    add_dicom_conversion_subparser,
)
from mircat_v2.dbase import add_dbase_subparser, create_database
from mircat_v2.segmentation import (
    add_segmentation_subparser,
    segment_nifti_files,
    update_models_config,
    add_models_to_mircat,
    list_mircat_models,
)
from mircat_v2.stats import add_stats_subparser, run_stats

__version__ = "0.1.0"


def main() -> None:
    """Mirshahi Lab CT Analysis Toolkit (v2) CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Mirshahi Lab CT Analysis Toolkit (v2)"
    )
    verbose_parser = parser.add_mutually_exclusive_group()
    verbose_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Write debugging logs in the terminal.",
    )
    verbose_parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Reduce output logs in the terminal to only success and error messages.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    # Add all the subparsers
    add_dicom_conversion_subparser(subparsers)
    add_dbase_subparser(subparsers)
    add_segmentation_subparser(subparsers)
    add_stats_subparser(subparsers)
    # Parse the command line arguments
    args = parser.parse_args()
    logger_setup(args.verbose, args.quiet)
    # Handle the commands
    if args.command == "convert":
        convert_dicoms_to_nifti(args)
    elif args.command == "dbase":
        if args.dbase_command == "create":
            create_database(
                dbase_path=args.dbase_path,
                update=args.update,
                overwrite=args.overwrite,
                no_setup=args.no_setup,
            )
        elif args.dbase_command == "query":
            # Assuming you have a function to handle the query
            pass
        else:
            logger.error(f"Unknown dbase command: {args.dbase_command}")
            parser.print_help()
            exit(1)
    elif args.command == "segment":
        segment_nifti_files(args)
    elif args.command == "models":
        if args.models_command == "list":
            list_mircat_models(args)
        elif args.models_command == "update":
            update_models_config()
        elif args.models_command == "add":
            add_models_to_mircat(args)
    elif args.command == "stats":
        run_stats(args)
    else:
        logger.error(f"Unknown command: {args.command}")
        parser.print_help()
        exit(1)
