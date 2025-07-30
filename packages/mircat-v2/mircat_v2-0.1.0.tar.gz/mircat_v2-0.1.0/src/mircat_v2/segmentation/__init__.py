import sys
import json
import pprint

from math import floor
from multiprocessing import cpu_count
from pathlib import Path
from shutil import copytree
from loguru import logger

from mircat_v2.configs import (
    read_segmentation_config,
    read_dbase_config,
    segmentation_config_file,
    set_threads_per_process,
)
from mircat_v2.segmentation.segmentor import MircatSegmentor

lib_path = Path(__file__).parent.resolve()
models_path = lib_path / "models"


def add_segmentation_subparser(subparsers):
    """Add segmentation specific subcommands to mircat-v2
    :param subparsers: the subparser for CLI
    """
    # Add subcommands for segmentation itself
    seg_parser = subparsers.add_parser(
        "segment",
        description="""Segment nifti files using nnUNet - accelerated by GPU if available. \
            Input files will be resampled and stored in temporary files to accelerate nnUNet. \
            Make sure you have enough disk space for resampled images!""",
        help="Segment nifti files using nnUNet models.",
    )
    seg_parser.add_argument(
        "niftis",
        type=Path,
        help="Path to a nifti file or a text file containing a list of nifti files",
    )
    seg_parser.add_argument(
        "-tl",
        "--task-list",
        type=str,
        nargs="+",
        required=True,
        help="Space separated list of segmentation model tasks to perform. Identified by nnUNet dataset number. Use mircat-v2 models list to see all available tasks.",
    )
    seg_parser.add_argument(
        "-m",
        "--model-types",
        type=str,
        nargs="+",
        default=["3d"],
        choices=["2d", "3d", "3d_lowres", "3d_cascade"],
        help="Default = 3d for all tasks. The nnUNet model subtype to run for each task, space separated.",
    )
    seg_parser.add_argument(
        "-n",
        "--n-processes",
        type=int,
        default=1,
        help="Default = 1. Number of processes to use for pre/post processing the images.",
    )
    seg_parser.add_argument(
        "-t",
        "--threads-per-process",
        type=int,
        default=4,
        help="Default = 4. Maximum number of threads each process should use.",
    )
    seg_parser.add_argument(
        "-c",
        "--cache-size",
        type=int,
        default=10,
        help="The number of nifti files to work on at one time. Default = 10. This includes saving preprocessed files to disk, so be mindful of storage.",
    )
    seg_parser.add_argument(
        "-db",
        "--dbase-insert",
        action="store_true",
        help="Store model results (completed/failed for each nifti) in the mircat-v2 database. Must be setup!",
    )
    seg_parser.add_argument(
        "-ir",
        "--image-resampler",
        type=str,
        choices=["lanczos", "bspline", "gaussian", "linear"],
        default="bspline",
        help="Interpolator for resampling original images. Default = bspline (speed and quality balance)",
    )
    seg_parser.add_argument(
        "-lr",
        "--label-resampler",
        type=str,
        choices=["gaussian", "linear", "nearest"],
        default="gaussian",
        help="Interpolator for resampling segmentation images. Default = gaussian (slowest but best)",
    )
    # Model specific operations
    models_parser = subparsers.add_parser(
        "models",
        description="""List models available, copy new models to the correct mircat-v2 location, or update the config file for segmentation""",
        help="List, add or update models available to mircat-v2.",
    )
    models_subparser = models_parser.add_subparsers(dest="models_command")
    list_subparser = models_subparser.add_parser(
        "list",
        help="List tasks and their descriptions currently available to mircat-v2.",
    )
    list_subparser.add_argument(
        "-t",
        "--task",
        type=str,
        default="all",
        help="Specific task number to list configuration for. Default is to show all tasks.",
    )
    add_command = models_subparser.add_parser(
        "add",
        description="Add nnUNet model(s) to mircat-v2 options.",
        help="Add nnUNet model or folder of nnUNet models to mircat library",
    )
    add_command.add_argument(
        "folder",
        type=Path,
        help="Path to nnUNet model or folder containing multiple nnUNet models. \
            Should either be in the format DatasetXXX_* or be a folder containing folders in that format.",
    )
    add_command.add_argument(
        "--overwrite",
        action="store_true",
        help="If a model task already exists in the mircat models file, overwrite it.",
    )
    models_subparser.add_parser("update", help="Update the model configurations file.")


def segment_nifti_files(args):
    logger.debug(
        "Starting segmentation process with the following args:\n{}",
        pprint.pformat(args),
    )
    task_configs = read_segmentation_config()
    _validate_segmentation_args(task_configs, args)
    segmentor = MircatSegmentor(
        task_list=args.task_list,
        model_types=args.model_types,
        task_configs=task_configs,
        n_processes=args.n_processes,
        threads_per_process=args.threads_per_process,
        cache_size=args.cache_size,
        dbase_config=args.dbase_config,
        img_resampler=args.image_resampler,
        lbl_resampler=args.label_resampler,
    )
    segmentor.run(args.niftis)


def _get_available_models():
    task_folders = sorted(models_path.glob("Dataset*/"))
    logger.debug(
        """Found {} models in {}. They are:\n{}""",
        len(task_folders),
        str(models_path),
        pprint.pformat([str(x.name) for x in task_folders]),
    )
    if len(task_folders) == 0:
        raise FileNotFoundError(
            f"No folders found in {models_path}. Use mircat-v2 models copy to copy in some nnUNet models!"
        )
    return task_folders


def _validate_segmentation_args(task_configs: dict, args):
    """Internal function to validate the given arguments for nnUNet segmentation
    :param model_configs: the internal configuration file for mircat-v2 loaded as a dictionary
    :param args: the passed input parameters
    """
    # Make sure the input argument for the nifti file(s) exists
    args.niftis = args.niftis.resolve()
    if not args.niftis.exists():
        logger.error(
            f"The input nifti file/list of files {args.niftis} does not exist. Please double check your paths."
        )
        sys.exit(1)
    available_models = list(task_configs.keys())
    # Make sure all tasks are available
    if not all([task in available_models for task in args.task_list]):
        missing_tasks = [
            task for task in args.task_list if task not in available_models
        ]
        logger.error(
            "The following tasks are missing from mircat-v2 config file {}. Please use `mircat-v2 models add` to place them in the correct location.",
            missing_tasks,
        )
        sys.exit(1)
    # If only one model type was given, apply it for all tasks
    if len(args.model_types) == 1:
        model_type = args.model_types[0]
        logger.debug(
            "One model type passed to --model-types. Will apply for all given tasks."
        )
        args.model_types = [model_type for task in args.task_list]
    # Ensure that each task has a specified model type
    if len(args.model_types) != len(args.task_list):
        logger.error(
            f"Number of model type parameters must match the number of tasks. Currently have {len(args.model_types)} model types and {len(args.task_list)} tasks.\n\t\
            Please either specify one model type [3d, 2d, 3d_lowres, 3d_casade] for all tasks or have a specific model type for each task."
        )
        sys.exit(1)
    # Ensure that each task has weights for the specific model type
    for task, model in zip(args.task_list, args.model_types):
        model_weights = task_configs[task]["models"].get(model, dict())
        logger.debug(f"{task} configurations: {model_weights}")
        if not model_weights:
            logger.error(f"No {model} configuration found for task {task}.")
            sys.exit(1)
    # Check if the mircat-v2 dbase exists.
    if args.dbase_insert:
        dbase_config = read_dbase_config()
        dbase_path = Path(dbase_config["dbase_path"]).resolve()
        if not dbase_path.exists():
            logger.error(
                f"Database was set to {dbase_path}, but was not found. Please check path!"
            )
            sys.exit(1)
        logger.debug(f"mircat-v2 database found at {dbase_path}")
        args.dbase_config = dbase_config
    else:
        args.dbase_config = {}

    set_threads_per_process(args)


def update_models_config():
    # We call them tasks as this is the nnUNet style - Dataset###_descriptor
    task_folders = _get_available_models()
    logger.info(f"Updating {len(task_folders)} models configurations.")
    if not segmentation_config_file.parent.exists():
        logger.debug("Segmentation config file does not exist. Creating it.")
        config_data = {}
    else:
        logger.debug(
            f"Reading existing segmentation config file {segmentation_config_file}."
        )
        with segmentation_config_file.open() as f:
            config_data = json.load(f)
    # The keys here are what UNet calls each model type
    # The values are what we will use as flags to select a model
    unet_configs = {
        "2d": "2d",
        "3d_fullres": "3d",
        "3d_lowres": "3d_lowres",
        "3d_cascade_fullres": "3d_cascade",
    }
    for folder in task_folders:
        splits = folder.name.split("_")
        task = splits[0].replace("Dataset", "")
        description = "_".join(splits[1:])
        task_models = sorted(folder.glob("*/"))
        logger.debug(f"Task: {task}, Models: {task_models}")
        task_config = {"description": description, "models": {}}
        if len(task_models) == 0:
            logger.warning(f"No model options found in {folder}.")
            continue
        # Pull a reference model
        ref_model = task_models[0]
        if not (ref_model / "dataset.json").exists():
            logger.error(f"No dataset info found for {folder}. Skipping.")
            continue
        if not (ref_model / "plans.json").exists():
            logger.error(f"No model plans found for {folder}. Skipping.")
        with (ref_model / "dataset.json").open() as f:
            dataset = json.load(f)
        with (ref_model / "plans.json").open() as f:
            plans = json.load(f)
            configs = plans["configurations"]
        labels = dataset.get("labels")
        task_config["labels"] = labels
        # Get all of the nnUNet model options for the task that are available.
        for unet_config, option in unet_configs.items():
            for model in task_models:
                if unet_config in model.name:
                    model_specific_config = configs.get(unet_config)
                    task_config["models"][option] = {
                        "path": str(model),
                        "patch_size": model_specific_config.get("patch_size"),
                        "spacing": model_specific_config.get("spacing"),
                    }
        config_data[task] = task_config
    with segmentation_config_file.open("w") as f:
        json.dump(config_data, f, indent=4)
    logger.success(
        f"mircat-v2 model configs successfully updated. View them at {segmentation_config_file}."
    )


def add_models_to_mircat(args) -> None:
    folder: Path = args.folder
    overwrite: bool = args.overwrite
    if overwrite:
        confirmed = input(
            "Overwrite option was given to copy command. Are you sure you want to overwrite existing models? (y/n) "
        )
        confirmed = confirmed == "y"
        if not confirmed:
            logger.info("Aborting copy operation.")
            return

    folder = folder.resolve()
    if not folder.is_dir():
        logger.error(
            f"Given path {folder} is not a folder. Please make sure you are passing an nnUNet folder."
        )
        return
    if not any(folder.iterdir()):
        logger.error(
            f"Folder {folder} is empty. Please check that your path is correct."
        )
        return
    if folder.name.startswith("Dataset"):
        logger.info(f"Found 1 model to copy: {folder}")
        logger.info(f"Copying {folder} to {models_path}")
        destination = models_path / folder.name
        copytree(folder, destination, dirs_exist_ok=overwrite)
        logger.success(
            f"{folder} succesfully copied to mircat-v2 models. Updating config."
        )
    else:
        models = list(folder.glob("*/Dataset*"))
        n_models = len(models)
        if n_models == 0:
            logger.error(
                f"No models found in {folder}. Please make sure the input is either of format 'DatasetXXX_*' or folder/DatasetXXX_*"
            )
            return
        model_tasks = {
            model.name.split("_")[0].replace("Dataset", ""): model for model in models
        }
        logger.info(
            f"Found {n_models} models to copy in {folder} - Task numbers are {', '.join(model_tasks.keys())}"
        )
        for i, (task, model_path) in enumerate(model_tasks.items(), start=1):
            destination = models_path / model_path.name
            copytree(model_path, destination, dirs_exist_ok=overwrite)
            logger.success(
                f"{i}/{n_models} - Succesfully copied task {task} from {model_path} to mircat library."
            )
        logger.info("All models copied. Updating config.")
    update_models_config()


def list_mircat_models(args):
    with segmentation_config_file.open() as f:
        configs = json.load(f)
    if args.task == "all":
        pprint.pprint(configs, indent=2, sort_dicts=False)
        return
    else:
        subdict = configs.get(args.task)
        if subdict is None:
            logger.error(
                f"Task number {args.task} not found in model configs. Available tasks are\n\t{list(configs.keys())}",
            )
            return
        pprint.pprint(subdict, indent=2, sort_dicts=False)
