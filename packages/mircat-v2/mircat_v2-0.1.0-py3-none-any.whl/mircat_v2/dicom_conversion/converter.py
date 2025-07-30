import json
import traceback
from datetime import date
from pathlib import Path
from multiprocessing import Pool
from shutil import copyfile

import dicom2nifti
import dicom2nifti.settings as settings
from dicom2nifti.convert_dir import _remove_accents
import numpy as np
from pydicom import dcmread
from loguru import logger
from threadpoolctl import threadpool_limits

from ..dbase import insert_data_batch, dbase_config_file


class DicomConverter:
    """Class to convert DICOM files to NIfTI format using the dicom2nifti library.
    This class provides options for resampling, validation, and parallel processing.
    The output NIfTI files are saved in a specified directory with subdirectories based on the input DICOM file's metadata.
    """

    def __init__(
        self,
        axial_only: bool = False,
        no_mip: bool = False,
        resample: bool = True,
        resample_spline_interpolation_order: int = 3,
        resample_padding: int = -1024,
        validate_orthogonal: bool = False,
        n_processes: int = 1,
        threads_per_process: int = 4,
        min_slice_count: int = 30,
        db_batch_size: int = 100,
    ):
        """
        Initialize the DicomConverter with optional resampling settings.

        Args:
            axial_only (bool): Whether to only convert axial series. Default is False.
            no_mip (bool): Whether to skip converting MIP series. Default is False.
            resample (bool): Whether to resample the DICOM images to standard LAS orientation. Default is True.
            resample_spline_interpolation_order (int): The order of the spline interpolation for resampling. Default is 3.
            resample_padding (int): The padding value for resampling. Default is -1024 (Hounsfield units).
            validate_orthogonal (bool): Whether to validate the orthogonality of the DICOM images. Default is False.
                If True, gantry tilted images will not be converted.
            n_processes (int): The number of processes to use for conversion. Default is 1.
            threads_per_process (int): The maximum number of threads to use for conversion in each process. Default is 4.
            min_file_count (int): The minimum number of DICOM files in a folder required to perform conversion. Default is 30.
            db_batch_size (int): The number of records to insert into the database at once if it exists. Default is 100.
        """
        # Set the conversion options
        self.axial_only = axial_only
        self.no_mip = no_mip
        self.n_processes = n_processes
        self.threads_per_process = threads_per_process
        self.min_slice_count = min_slice_count
        self.db_batch_size = db_batch_size
        # Set the resampling options for the dicom2nifti library
        settings.resample = resample
        settings.resample_spline_interpolation_order = (
            resample_spline_interpolation_order
        )
        settings.resample_padding = resample_padding
        settings.validate_orthogonal = validate_orthogonal
        if dbase_config_file.exists():
            logger.info("Database configuration file found. Loading...")
            with dbase_config_file.open("r") as f:
                self.dbase_config = json.load(f)
        else:
            self.dbase_config = {}

    def convert(
        self, dicom_folders: list[str | Path], output_directory: str | Path
    ) -> None:
        """
        Convert DICOM files to NIfTI format.

        Args:
            dicom_folders (list[str|Path]): A list of DICOM folders to convert.
            output_directory (str|Path): Directory to save the converted NIfTI files.
        """
        # Validate the input dicom folders
        if not isinstance(dicom_folders, list):
            raise TypeError("dicom_folders must be a list of folder paths.")
        num_folders = len(dicom_folders)
        if num_folders == 0:
            raise ValueError("dicom_folders list is empty.")
        # Create the base output directory if it doesn't exist
        self.output_directory = Path(output_directory).resolve()
        if not self.output_directory.exists():
            logger.info(f"Creating output directory: {self.output_directory}")
            self.output_directory.mkdir(parents=True, exist_ok=True)
        # Run the conversion in parallel using multiprocessing
        if self.n_processes > num_folders:
            logger.info(
                f"Number of processes ({self.n_processes}) is greater than number of folders ({num_folders}). Setting number of processes to {num_folders}."
            )
            self.n_processes = num_folders
        logger.info(
            f"Running in {self.n_processes} process{'es' if self.n_processes > 1 else ''}."
        )
        completed = 1
        metadata_batch = []
        with Pool(self.n_processes) as pool:
            # We use imap_unordered because we don't care about the order of completion
            for result in pool.imap_unordered(self.convert_folder, dicom_folders):
                if result is not None:
                    dicom_folder, output_nifti, metadata = result
                    metadata["output_nifti"] = str(output_nifti)
                    metadata["conversion_date"] = date.today().strftime("%Y-%m-%d")
                    logger.success(
                        f"{completed}/{num_folders} - Converted {dicom_folder} to {output_nifti}",
                        extra={"folder": dicom_folder, "output": output_nifti},
                    )
                    if self.dbase_config and metadata:
                        metadata_batch.append(metadata)
                        if len(metadata_batch) >= self.db_batch_size:
                            insert_data_batch(
                                self.dbase_config,
                                "conversions",
                                metadata_batch,
                            )
                            metadata_batch = []
                completed += 1
        # Insert any remaining metadata into the database
        if self.dbase_config and metadata_batch:
            insert_data_batch(
                self.dbase_config,
                "conversions",
                metadata_batch,
            )

    def convert_folder(self, dicom_folder: str | Path) -> tuple[str, str] | None:
        """
        Wrapper of _convert_folder to handle exceptions and logging.
        Args:
            dicom_folder (str): Path to the DICOM folder to convert.
        Returns:
            tuple[str, str]: The input DICOM folder and output nifti file path.
        """
        try:
            return self._convert_folder(dicom_folder)
        except Exception as e:
            logger.error(
                f"Error converting folder {dicom_folder}: {e}\n{traceback.format_exc()}",
                extra={"folder": dicom_folder, "error": str(e)},
            )
            return None

    def _convert_folder(self, dicom_folder: str | Path) -> tuple[str, str]:
        """
        Convert a single DICOM folder to NIfTI format.

        Args:
            dicom_folder (str): Path to the DICOM folder to convert.
        Returns:
            tuple[str, str]: The input DICOM folder and output nifti file path.
        """
        with threadpool_limits(limits=self.threads_per_process):
            dicom_folder = Path(dicom_folder).resolve()
            if not dicom_folder.exists():
                raise FileNotFoundError(f"DICOM folder does not exist: {dicom_folder}")
            if not dicom_folder.is_dir():
                raise NotADirectoryError(f"Path is not a directory: {dicom_folder}")
            dicom_files = list(dicom_folder.glob("*.dcm"))
            if len(dicom_files) == 0:
                logger.warning(f"No DICOM files found in folder: {dicom_folder}")
                return
            if len(dicom_files) < self.min_slice_count:
                logger.warning(
                    f"Skipping folder {dicom_folder} with less than {self.min_slice_count} DICOM files."
                )
                return
            # Get the metadata from the DICOM files
            reference_dicom = dicom_files[0]
            metadata = self._get_metadata(reference_dicom)
            if metadata.get("series_name") == "nan":
                logger.warning(
                    f"Skipping folder {dicom_folder} due to series_name == 'nan'."
                )
                return
            if "ai-rad_companion" in metadata.get("series_name"):
                logger.warning(
                    f"Skipping AI-Rad companion report series {metadata.get('original_series_name')} in folder {dicom_folder}."
                )
                return
            if self.axial_only and metadata.get("ct_direction") != "AX":
                logger.warning(
                    f"Skipping non-axial series {metadata.get('original_series_name')} in folder {dicom_folder}."
                )
                return
            if self.no_mip:
                # Do a check for MIP series
                if (
                    "mip" in metadata.get("series_name").lower()
                    or metadata.get("slice_thickness_mm", 5) > 5
                ):
                    logger.warning(
                        f"Skipping likely MIP series {metadata.get('original_series_name')} in folder {dicom_folder}."
                    )
                    return
            output_nifti = (
                f"{metadata['series_number']}_{metadata['series_name']}.nii.gz"
            )
            custom_output_directory = (
                self.output_directory
                / metadata.get("mrn")[:2]  # First 2 numbers of MRN
                / metadata.get("mrn")[2:4]  # Next 2 numbers of MRN
                / metadata.get("mrn")
                / metadata.get("accession")
                / metadata.get("series_name")
            )
            if not custom_output_directory.exists():
                custom_output_directory.mkdir(parents=True, exist_ok=True)
            # Convert the DICOM files to NIfTI format
            dicom2nifti.convert_directory(dicom_folder, custom_output_directory)
            # Save the metadata to a JSON file
            metadata_file = custom_output_directory / "metadata.json"
            with metadata_file.open("w") as f:
                json.dump(metadata, f, indent=4)
            # Copy the reference DICOM file to the output directory
            dicom_file = custom_output_directory / reference_dicom.name
            copyfile(reference_dicom, dicom_file)
            return dicom_folder, custom_output_directory / output_nifti, metadata

    def _get_metadata(self, reference_dicom: Path) -> dict:
        """Get the metadata from a DICOM file that is not saved in the NIfTI header.
        Args:
            reference_dicom (Path): Path to the reference DICOM file.
        Returns:
            dict: A dictionary containing the metadata.
        """
        orientations = {
            "COR": [1, 0, 0, 0, 0, -1],
            "SAG": [0, 1, 0, 0, 0, -1],
            "AX": [1, 0, 0, 0, 1, 0],
        }
        meta_attributes = {
            "PatientID": "mrn",
            "AccessionNumber": "accession",
            "SeriesDescription": "series_name",
            "SeriesNumber": "series_number",
            "StudyDescription": "study_description",
            "ImageOrientationPatient": "ct_direction",
            "ImageType": "image_type",
            "PatientSex": "sex",
            "PatientAge": "age",
            "PatientSize": "height_m",
            "PatientWeight": "weight_kg",
            "PregnancyStatus": "pregnancy_status",
            "PatientBirthDate": "birth_date",
            "AcquisitionDate": "scan_date",
            "PixelSpacing": None,
            "SliceThickness": "slice_thickness_mm",
            "Manufacturer": "manufacturer",
            "ManufacturerModelName": "model",
            "KVP": "kvp",
            "SequenceName": "sequence_name",
            "ProtocolName": "protocol_name",
            "ContrastBolusAgent": "contrast_bolus_agent",
            "ContrastBolusRoute": "contrast_bolus_route",
            "ContrastBolusVolume": "contrast_bolus_volume",
            "StudyInstanceUID": "study_uid",
            "SeriesInstanceUID": "series_uid",
            "Modality": "modality",
        }
        metadata = {}
        try:
            ref = dcmread(reference_dicom)
        except FileNotFoundError:
            logger.error(f"Reference DICOM file not found: {reference_dicom}")
            return metadata
        except Exception as e:
            logger.error(f"Error reading DICOM file {reference_dicom}: {e}")
            return metadata
        # Need these 3 fields to create the output directory
        if not hasattr(ref, "PatientID"):
            raise ValueError(
                f"Reference DICOM file does not have PatientID: {reference_dicom.parent}"
            )
        if not hasattr(ref, "AccessionNumber"):
            raise ValueError(
                f"Reference DICOM file does not have AccessionNumber: {reference_dicom.parent}"
            )
        if not hasattr(ref, "SeriesDescription"):
            raise ValueError(
                f"Reference DICOM file does not have SeriesDescription: {reference_dicom.parent}"
            )
        # Go through the metadata attributes and get the values
        for tag, column in meta_attributes.items():
            if not hasattr(ref, tag):
                # Not every DICOM file has all the tags, so we skip them
                continue
            value = getattr(ref, tag)
            match tag:
                case "PatientID":
                    value = str(value).zfill(0)
                case "SeriesDescription":
                    # Remove accents from the SeriesDescription
                    metadata["original_series_name"] = value
                    value = _remove_accents(value)
                case "SeriesNumber":
                    value = int(value)
                case "ImageOrientationPatient":
                    value = [round(float(x)) for x in value]
                    for orientation, array in orientations.items():
                        if np.allclose(value, array):
                            value = orientation
                            break
                    if isinstance(value, list):
                        value = "AX"
                    if isinstance(value, str) and value not in orientations:
                        value = "AX"
                case "ImageType":
                    value = "_".join(value)
                case tag if tag in ["PatientBirthDate", "AcquisitionDate"]:
                    value = date.fromisoformat(value).strftime("%Y-%m-%d")
                case "PatientAge":
                    value = int(value[:-1])
                case "PixelSpacing":
                    length, width = value
                    metadata["pixel_length_mm"] = float(length)
                    metadata["pixel_width_mm"] = float(width)
                    continue
                case "PregnancyStatus":
                    value = int(value)
                    if value == 4:
                        value = None
                    elif value == 1:
                        value = 0
                    elif value == 2:
                        value = 1
                    elif value == 3:
                        value = 2
                case tag if tag in [
                    "PatientSize",
                    "PatientWeight",
                    "KVP",
                    "SliceThickness",
                ]:
                    value = float(value)
                case tag if tag in ["SequenceName", "ProtocolName"]:
                    value = str(value).lower()
                case _:
                    pass
            if value == "":
                value = None
            metadata[column] = value
        if not metadata:
            raise ValueError(
                f"Reference DICOM file does not have any metadata: {reference_dicom.parent}"
            )
        if metadata.get("slice_thickness_mm") is None:
            metadata["slice_thickness_mm"] = 5
        metadata["dicom_folder"] = str(reference_dicom.parent)
        return metadata
