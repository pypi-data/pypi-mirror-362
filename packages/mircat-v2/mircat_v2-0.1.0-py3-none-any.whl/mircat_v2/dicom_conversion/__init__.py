from .converter import DicomConverter
from pathlib import Path


def convert_dicoms_to_nifti(convert_args):
    """Convert dicom files to NIfTI format.
    Args:
        convert_args (argparse.Namespace): Arguments from the command line.
    """
    converter = DicomConverter(
        axial_only=convert_args.axial_only,
        no_mip=convert_args.no_mip,
        resample=not convert_args.no_resampling,
        resample_spline_interpolation_order=convert_args.resample_interpolation_order,
        resample_padding=convert_args.resample_padding,
        validate_orthogonal=convert_args.validate_orthogonal,
        n_processes=convert_args.n_processes,
        threads_per_process=convert_args.threads_per_process,
        min_slice_count=convert_args.min_slice_count,
        db_batch_size=convert_args.db_batch_size,
    )
    if convert_args.dicoms.is_file():
        # If the input is a file, read the list of dicom directories from the file
        with convert_args.dicoms.open() as f:
            dicom_folders = [Path(line.strip()) for line in f.readlines()]
    else:
        # If the input is a directory, use it as the list of dicom directories
        dicom_folders = [convert_args.dicoms]
    converter.convert(
        dicom_folders=dicom_folders,
        output_directory=convert_args.output_dir,
    )


def add_dicom_conversion_subparser(subparsers):
    # Add subcommands
    convert_parser = subparsers.add_parser(
        "convert", help="Convert dicom data to the NIfTI format"
    )
    convert_parser.add_argument(
        "dicoms",
        help="Path to a dicom directory or a file containing a list of dicom directories",
        type=Path,
    )
    convert_parser.add_argument(
        "output_dir",
        type=Path,
        help="Path to the output directory",
    )
    convert_parser.add_argument(
        "--n-processes",
        "-n",
        type=int,
        default=1,
        help="Number of processes to use for conversion (default: 1)",
    )
    convert_parser.add_argument(
        "--threads-per-process",
        "-t",
        type=int,
        default=4,
        help="Maximum number of transformation threads per process (default: 4)",
    )
    convert_parser.add_argument(
        "--axial-only",
        "-ax",
        action="store_true",
        help="Only convert axial series",
    )
    convert_parser.add_argument(
        "--no-mip", "-nm", action="store_true", help="Do not convert MIP series"
    )
    convert_parser.add_argument(
        "--no-resampling",
        "-nr",
        action="store_true",
        help="Do not resample the dicoms to LAS orientation",
    )
    convert_parser.add_argument(
        "--resample-interpolation-order",
        "-i",
        type=int,
        default=3,
        help="Interpolation order for resampling (default: 3)",
    )
    convert_parser.add_argument(
        "--resample-padding",
        "-p",
        type=int,
        default=-1024,
        help="Padding Hounsfield Unit for resampling (default: -1024)",
    )
    convert_parser.add_argument(
        "--validate-orthogonal",
        "-v",
        action="store_true",
        help="Validate that the dicoms are orthogonal. Will not convert gantry tilted series.",
    )
    convert_parser.add_argument(
        "--min-slice-count",
        "-s",
        type=int,
        default=30,
        help="Minimum number of slices to consider a series valid (default: 30)",
    )
    convert_parser.add_argument(
        "--db-batch-size",
        "-b",
        type=int,
        default=100,
        help="Batch size for database insertion (default: 100)",
    )
