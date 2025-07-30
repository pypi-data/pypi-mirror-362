import json
import SimpleITK as sitk
from pathlib import Path
from loguru import logger
from multiprocessing import Pool
from threadpoolctl import threadpool_limits
from mircat_v2.configs import read_dbase_config, read_segmentation_config
from mircat_v2.nifti import StatsNifti
from mircat_v2.stats.vol_int import calculate_volume_and_intensity_stats
from mircat_v2.stats.contrast import predict_contrast
from mircat_v2.stats.vertebrae import calculate_vertebrae_stats


class Analyzer:
    """Analyzer class for processing and analyzing tasks with specified parameters."""

    # Map for resolution settings
    resolution_map = {
        "normal": [1.0, 1.0, 1.0],
        "high": [0.75, 0.75, 0.75],
        "highest": [0.5, 0.5, 0.5],
    }
    # Segmentations needed for specific tasks in order of preference
    task_map = {
        "vol-int": ["999"],
        "contrast": ["999"],
        "vertebrae": ["999"],
        "aorta": ["999"],
        "tissues": ["485", "481"],
        # FIXME - need to add body segmentation id to tissues
    }

    def __init__(
        self,
        task_list: list[str],
        resolution: str,
        image_resampler: str,
        label_resampler: str,
        n_processes: int,
        threads_per_process: int,
        dbase_insert: bool = False,
        overwrite: bool = False,
    ):
        if task_list == ["all"]:
            task_list = list(self.task_map.keys())
        # This orders the tasks by the order they are defined in task_map
        self.task_list = [task for task in self.task_map if task in task_list]
        self.resolution = self.resolution_map.get(resolution)
        self.image_resampler = image_resampler
        self.label_resampler = label_resampler
        self.n_processes = n_processes
        self.threads_per_process = threads_per_process
        # Read database configuration if dbase_insert is True
        self.dbase_insert = dbase_insert
        if dbase_insert:
            self.dbase_config = read_dbase_config()
        else:
            self.dbase_config = {}
        # Read segmentation configuration
        seg_config = read_segmentation_config()
        # We only need the labels for each task
        self.segmentation_labels = {
            task: seg_config[task]["labels"] for task in seg_config
        }
        self.overwrite = overwrite

    def run(self, niftis: Path | str) -> None:
        """Run the analysis on the provided NiFTi files.
        :param niftis: Path to a nifti file with mircat-v2 segmentations or a text file with a list of multiple mircat-v2 nifti files.
        """
        self._get_nifti_list(niftis)
        if self.n_processes > 1:
            logger.info(f"Running analysis with {self.n_processes} processes.")
        else:
            logger.info("Running analysis with single process.")
        logger.info(
            f"Using resolution: {self.resolution} mm, image resampler: {self.image_resampler}, label resampler: {self.label_resampler}."
        )
        logger.info(f"Tasks to run: {self.task_list}.")
        logger.info(f"Starting analysis on {self.total_niftis} nifti files.")
        batch_data = []
        with Pool(processes=self.n_processes) as pool:
            for i, nifti in enumerate(
                pool.imap_unordered(self.analyze, self.niftis), start=1
            ):
                logger.success(
                    f"Stats: [{i}/{self.total_niftis}] - Successfully calculated statistics for {nifti.name}."
                )
                batch_data.append(nifti.stats)
                if i % 100 == 0 and self.dbase_insert:
                    logger.info("inserting batch of 100 nifti files into the database.")
                    # TODO Logic to insert batch_data into the database
                    batch_data.clear()
        if self.dbase_insert and batch_data:
            logger.info("inserting remaining nifti files into the database.")
            # TODO Logic to insert remaining batch_data into the database
            logger.info(batch_data)

    def _get_nifti_list(self, niftis):
        niftis = Path(niftis).resolve()
        if not niftis.exists():
            raise FileNotFoundError(f"Nifti file {niftis} does not exist.")
        if niftis.suffix in [".nii", ".gz"]:
            self.niftis = [niftis]
        else:
            with niftis.open() as f:
                self.niftis = [Path(line.strip()).resolve() for line in f.readlines()]
        self.total_niftis = len(self.niftis)
        if self.total_niftis == 0:
            raise ValueError("No valid nifti files found in the provided path or file.")
        logger.info(f"Found {self.total_niftis} nifti files to process from {niftis}.")

    def analyze(self, nifti_path: Path | str) -> StatsNifti:
        """Analyze a single nifti file.
        :param nifti_path: Path to the nifti file to analyze.
        """
        sitk.ProcessObject.SetGlobalDefaultNumberOfThreads(self.threads_per_process)
        with threadpool_limits(self.threads_per_process):
            nifti = StatsNifti(nifti_path, self.overwrite)
            # Preprocess the nifti file for statistics
            (
                nifti.check_for_segmentations(
                    self.task_list, self.task_map
                ).preprocess_for_stats(
                    self.resolution, self.image_resampler, self.label_resampler
                )
            )
            self.analyze_tasks(nifti)
        nifti.save_json_stats()
        return nifti

    def analyze_tasks(self, nifti: StatsNifti) -> None:
        for task in self.task_list:
            seg_id = nifti.task_to_id_map[task]
            seg_labels = self.segmentation_labels[seg_id]
            match task:
                case "vol-int":
                    vol_int_stats = calculate_volume_and_intensity_stats(
                        nifti, seg_id, seg_labels
                    )
                    nifti.add_stats("vol-int", vol_int_stats)
                case "contrast":
                    if not nifti.stats.get("vol-int", {}):
                        logger.warning(
                            "Organ intensities are needed for contrast prediction. Skipping contrast task."
                        )
                        continue
                    contrast_stats = predict_contrast(nifti.stats["vol-int"])
                    nifti.add_stats("contrast", contrast_stats)
                case "vertebrae":
                    vertebrae_stats = calculate_vertebrae_stats(
                        nifti, seg_id, seg_labels
                    )
                    nifti.add_stats("vertebrae", vertebrae_stats)
                    nifti.set_vertebrae_midlines(vertebrae_stats)
                # TODO: Implement other tasks as needed
