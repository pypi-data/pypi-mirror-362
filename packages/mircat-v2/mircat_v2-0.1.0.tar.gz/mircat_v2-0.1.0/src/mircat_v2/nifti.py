import json
import traceback
import SimpleITK as sitk

from pathlib import Path
from loguru import logger


class Nifti:
    """A class used to represent a nifti file for mircat-v2 - including spacing, metadata, segmentations and others!"""

    def __init__(self, nifti_path: str | Path):
        nifti_path = Path(nifti_path).resolve()
        if not nifti_path.exists():
            message = f"Nifti file not found at {nifti_path}! Please check existence."
            logger.error(message)
            raise FileNotFoundError()
        if ".nii" not in nifti_path.suffixes:
            message = f"Input {nifti_path} not recognized as a nifti file. Please ensure file suffix is *.nii or *.nii.gz"
            logger.error(message)
            raise NotNiftiFileError()
        self.path = nifti_path
        self.parent = nifti_path.parent
        self.name = nifti_path.with_suffix("").stem
        self.seg_folder = self.parent / f"{self.name}_segs"
        self.segmentations = list(self.seg_folder.glob(f"{self.name}*.nii.gz"))
        try:
            self.img = sitk.ReadImage(nifti_path)
        except Exception as e:
            logger.error(
                f"Error loading {nifti_path} with SimpleITK :{e}\n{traceback.format_exc()}"
            )
            raise SimpleITKReadError()
        self.spacing = self.img.GetSpacing()
        self.shape = self.img.GetSize()
        if (nifti_path.parent / "metadata.json").exists():
            logger.debug(
                f"{nifti_path.parent / 'metadata.json'} found. Loading metadata."
            )
            with (nifti_path.parent / "metadata.json").open() as f:
                self.metadata: dict = json.load(f)
        else:
            logger.debug(
                f"No metadata.json file found next to {nifti_path}. Setting metadata to empty dictionary."
            )
            self.metadata: dict = {}


class SegNifti(Nifti):
    def __init__(self, nifti_path: str | Path):
        super().__init__(nifti_path)
        self.task_files: dict = {}

    def resample_and_save_for_segmentation(
        self, new_spacing, output_path, interpolator_type
    ) -> None:
        if len(new_spacing) == 2:
            # Set the new spacing z-length to be the same as the original
            new_spacing = [*new_spacing, self.spacing[-1]]
        # Resample image - always not a label
        resampled = resample_with_sitk(
            self.img,
            new_spacing=new_spacing,
            is_label=False,
            interpolator_type=interpolator_type,
        )
        sitk.WriteImage(resampled, output_path)
        logger.debug("Successfully resampled and wrote to {}", output_path)


class StatsNifti(Nifti):
    def __init__(self, nifti_path: str | Path, overwrite: bool = False):
        super().__init__(nifti_path)
        stats_file = self.seg_folder / f"{self.name}_stats.json"
        self.stats_file = stats_file
        if stats_file.exists() and not overwrite:
            logger.debug(f"Stats file {stats_file} found. Loading statistics.")
            with stats_file.open() as f:
                self.stats = json.load(f)
        else:
            if not overwrite:
                logger.debug(
                    f"No stats file found at {stats_file}. Setting stats to empty dictionary."
                )
            else:
                logger.debug(
                    f"Stats file {stats_file} exists but overwrite is set to True. Initializing empty stats."
                )
            self.stats = {}
        self.add_stats("nifti", str(self.path))
        if self.metadata != {}:
            logger.debug(f"Merging metadata with stats for {self.name}.")
            self.add_stats("series_uid", self.metadata.get("series_uid", "missing"))
            self.add_stats("metadata", dict(self.metadata))

    def set_task_to_id_map(self, task_to_id_map: dict) -> None:
        self.task_to_id_map = task_to_id_map
        return self

    def set_id_to_seg_map(self, id_to_seg_map: dict) -> None:
        """Set the mapping of task IDs to task names for this nifti."""
        self.id_to_seg_map = id_to_seg_map
        return self

    def set_vertebrae_midlines(self, vertebrae_stats: dict = None):
        """Set the vertebrae midlines for this nifti."""
        if vertebrae_stats is None:
            if "vertebrae" not in self.stats:
                logger.warning(
                    "No vertebrae stats found in nifti. Cannot set vertebrae midlines."
                )
                return self
            vertebrae_stats = self.stats["vertebrae"]
        vertebrae_midlines = {
            k: v.get("midline")
            for k, v in vertebrae_stats.items()
            if isinstance(v, dict)
        }
        self.vertebrae_midlines = vertebrae_midlines
        return self

    def add_stats(self, key: str, value: any) -> None:
        """Add a key-value pair to the stats dictionary."""
        if key in self.stats:
            logger.debug(
                f"Key {key} already exists in stats for {self.path}. Overwriting value."
            )
        self.stats[key] = value
        return self

    def preprocess_for_stats(
        self, new_spacing, image_resampler, label_resampler
    ) -> None:
        logger.debug(
            "Resampling image and segmentations for nifti {} to new spacing {}",
            self.name,
            new_spacing,
        )
        self.img = resample_with_sitk(
            self.img,
            new_spacing=new_spacing,
            is_label=False,
            interpolator_type=image_resampler,
            reorient="LAI",
        )
        self.spacing = self.img.GetSpacing()
        self.shape = self.img.GetSize()
        self.add_stats("stats_resolution", new_spacing)
        new_id_to_seg_map = {}
        for seg_id, seg_path in self.id_to_seg_map.items():
            logger.debug(
                "Resampling segmentation for seg_id {} at path {}", seg_id, seg_path
            )
            label = sitk.ReadImage(seg_path)
            resampled_label = resample_with_sitk(
                label,
                is_label=True,
                interpolator_type=label_resampler,
                reference_image=self.img,
            )
            assert resampled_label.GetSize() == self.img.GetSize(), (
                f"Resampled label size {resampled_label.GetSize()} does not match image size {self.img.GetSize()}"
            )
            new_id_to_seg_map[seg_id] = resampled_label
        self.set_id_to_seg_map(new_id_to_seg_map)
        return self

    def check_for_segmentations(self, task_list, task_map):
        task_to_id_map = {}
        id_to_segmentation_map = {}
        for task in task_list:
            allowed_segmentations = task_map.get(task, [])
            for seg_id in allowed_segmentations:
                seg_file = f"{self.name}_{seg_id}.nii.gz"
                if seg_file in [seg.name for seg in self.segmentations]:
                    task_to_id_map[task] = seg_id
                    id_to_segmentation_map[seg_id] = self.seg_folder / seg_file
        self.set_task_to_id_map(task_to_id_map)
        self.set_id_to_seg_map(id_to_segmentation_map)
        return self

    def save_json_stats(self):
        """Save the statistics to a JSON file."""
        save_stats = {k: v for k, v in self.stats.items() if "-db" not in k}
        with self.stats_file.open("w") as f:
            json.dump(save_stats, f, indent=4)


def resample_with_sitk(
    image,
    new_spacing=None,
    new_size=None,
    is_label=False,
    interpolator_type="gaussian",
    reference_image=None,
    reorient=None,
) -> sitk.Image:
    """Resample a SimpleITK image to a new spacing, size, or reference image.
    :param image: The SimpleITK image to resample.
    :param new_spacing: The new spacing to resample to. If None, the original
        spacing will be used to calculate the new size.
    :param new_size: The new size to resample to. If None, the original
        size will be used to calculate the new spacing.
    :param is_label: Whether the image is a label image. If True, the
        resampling will use label-specific interpolators.
    :param interpolator_type: The type of interpolator to use for resampling.
        Options are 'gaussian', 'linear', 'nearest' for label images, and
        'lanczos', 'bspline', 'gaussian', 'linear' for regular images.
    :param reference_image: An optional reference image to use for resampling.
        If provided, the new spacing and size will be taken from this image.
    :param reorient: The CT orientation to reorient the image to. If None, no reorientation is applied.
    :return: The resampled SimpleITK image."""
    # Get original properties
    original_spacing = image.GetSpacing()
    original_size = image.GetSize()

    resampler = sitk.ResampleImageFilter()
    if reference_image is not None:
        resampler.SetReferenceImage(reference_image)
    else:
        if new_spacing is not None and new_size is not None:
            raise ValueError("Only one of new_spacing and new_size may be specified")
        # Calculate new size based on spacing change
        if new_spacing is not None:
            new_size = [
                int(original_size[i] * original_spacing[i] / new_spacing[i])
                for i in range(3)
            ]
        elif new_size is not None:
            new_spacing = [
                original_spacing[i] * original_size[i] / new_size[i] for i in range(3)
            ]
        else:
            raise ValueError("Must specify either a new_size or new_spacing")
        #    Set up resampling parameters
        resampler.SetOutputSpacing(new_spacing)
        resampler.SetSize(new_size)
        resampler.SetOutputDirection(image.GetDirection())
        resampler.SetOutputOrigin(image.GetOrigin())
        resampler.SetTransform(sitk.Transform())
        resampler.SetDefaultPixelValue(0)

    if is_label:
        if interpolator_type == "gaussian":
            interpolator = sitk.sitkLabelGaussian
        elif interpolator_type == "linear":
            interpolator = sitk.sitkLabelLinear
        elif interpolator_type == "nearest":
            interpolator = sitk.sitkNearestNeighbor
        else:
            raise ValueError(
                f"label interpolator must be in [gaussian, linear, nearest], got {interpolator_type}"
            )
        resampler.SetInterpolator(interpolator)
    else:
        if interpolator_type == "lanczos":
            interpolator = sitk.sitkLanczosWindowedSinc
        elif interpolator_type == "bspline":
            interpolator = sitk.sitkBSpline
        elif interpolator_type == "gaussian":
            interpolator = sitk.sitkGaussian
        elif interpolator_type == "linear":
            interpolator = sitk.sitkLinear
        else:
            raise ValueError(
                f"image interpolator must be in [lanczos, gaussian, linear], got {interpolator_type}"
            )
        resampler.SetInterpolator(interpolator)
    resampled_image = resampler.Execute(image)
    if reorient is not None:
        current_orientation = (
            sitk.DICOMOrientImageFilter_GetOrientationFromDirectionCosines(
                resampled_image.GetDirection()
            )
        )
        if current_orientation != reorient:
            logger.debug(f"Reorienting image from {current_orientation} to {reorient}.")
            reorienter = sitk.DICOMOrientImageFilter()
            reorienter.SetDesiredCoordinateOrientation(reorient)
            resampled_image = reorienter.Execute(resampled_image)
    return resampled_image


class NotNiftiFileError(ValueError):
    pass


class SimpleITKReadError(ValueError):
    pass
