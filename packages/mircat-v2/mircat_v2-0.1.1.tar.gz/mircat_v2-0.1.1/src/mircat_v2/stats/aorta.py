import SimpleITK as sitk

from loguru import logger
from mircat_v2.stats.utilities import filter_segmentation
from mircat_v2.stats.vessel import Vessel


class Aorta(Vessel):
    """Class for aorta-specific statistics and operations for the custom segmentation model specifically."""

    anatomical_regions_vertebrae_map = {
        "thoracic": [f"T{i}" for i in range(3, 13)],
        "descending": [f"T{i}" for i in range(5, 13)],
        "upper_abdominal": ["T12", "L1", "L2"],
        "lower_abdominal": ["L2", "L3", "L4", "L5", "S1"],
    }

    def __init__(
        self,
        segmentation: sitk.Image,
        vertebrae_midlines: dict[str, int],
        label_map: dict,
    ):
        """
        Initialize the Aorta class with a nifti file and segmentation ID.
        :param nifti: StatsNifti object containing the nifti file and its metadata.
        :param seg_id: The segmentation ID to calculate statistics for.
        :param label_map: Dictionary mapping structure names to label IDs.
        """
        # We need to include the brachiocephalic trunk and left subclavian artery to separate anatomical regions
        labels = ["aorta", "brachiocephalic_trunk", "subclavian_artery_left"]
        self.segmentation = filter_segmentation(
            segmentation,
            labels=labels,
            label_map=label_map,
            remap=True,
            largest_connected_component=True,
        )
        self.anisotropy = list(self.segmentation.GetSpacing())
        self.array = sitk.GetArrayFromImage(self.segmentation)
        self.label_map = {idx: label for idx, label in enumerate(labels, start=1)}
        self.label = "aorta"
        self.label_idx = 1
        self.skeletonization_kwargs = {
            "teasar_params": {
                "scale": 1.0,
                "const": 40,
            },
            "object_ids": [1],  # Aorta is always label 1 in the segmentation
            "anisotropy": self.anisotropy,
            "dust_threshold": 1000,
            "progress": False,
            "fix_branching": True,
            "in_place": False,
            "fix_borders": True,
            "parallel": 1,
            "parallel_chunk_size": 100,
            "extra_targets_before": [],
            "extra_targets_after": [],
            "fill_holes": False,
            "fix_avocados": False,
            "voxel_graph": None,
        }
        self.vertebrae_midlines = vertebrae_midlines
        self._regions = None
        self.skeleton = None
        self.centerline = None
        self.cpr = None

    @property
    def regions(self):
        """
        Get the anatomical regions of the aorta.
        :return: Dictionary containing the anatomical regions and their properties.
        """
        if self._regions is None:
            self._determine_anatomical_regions()
        return self._regions

    def _determine_anatomical_regions(self):
        """
        Determine the anatomical regions of the aorta in the segmentation based on vertebrae midlines.
        """
        regions = {}
        for region, vertebrae in self.anatomical_regions_vertebrae_map.items():
            midlines = [
                self.vertebrae_midlines[vert]
                for vert in vertebrae
                if self.vertebrae_midlines.get(vert) is not None
            ]
            # Need at least two midlines to determine a region
            if len(midlines) > 1:
                regions[region] = {
                    "in_image": True,
                    "entire_region": len(midlines) == len(vertebrae),
                    "start": min(midlines),
                    "end": max(midlines),
                }
            else:
                regions[region] = {
                    "in_image": False,
                    "entire_region": False,
                    "start": None,
                    "end": None,
                }
        self._regions = regions
        return self


def calculate_aorta_stats(nifti, seg_id: str, label_map: dict) -> dict:
    """Calculate aorta specific statistics for a given nifti file.
    :param nifti: StatsNifti object containing the nifti file and its metadata.
    :param seg_id: The segmentation ID to calculate statistics for.
    :param label_map: Dictionary mapping structure names to label IDs.
    :return: Dictionary containing aorta specific statistics.
    """
    logger.debug(f"Calculating aorta stats for {nifti.name}.")
    if not hasattr(nifti, "vertebrae_midlines"):
        logger.warning(
            f"Vertebrae midlines not found in {nifti.name}. Skipping aorta stats calculation."
        )
        return {}
    segmentation = nifti.id_to_seg_map.get(seg_id)
    aorta = Aorta(
        segmentation,
        nifti.vertebrae_midlines,
        label_map,
    )
