import SimpleITK as sitk
from skimage.measure import label, regionprops


def _calculate_shape_stats(seg: sitk.Image) -> sitk.LabelShapeStatisticsImageFilter:
    """Calculate the shape stats for a segmentation
    Parameters
    ----------
    seg : sitk.Image
        The segmentation to calculate shape stats for
    Returns
    -------
    sitk.LabelShapeStatisticsImageFilter
        The executed shape stats
    """
    shape_stats = sitk.LabelShapeStatisticsImageFilter()
    shape_stats.SetGlobalDefaultCoordinateTolerance(1e-5)
    shape_stats.ComputeOrientedBoundingBoxOn()
    shape_stats.ComputePerimeterOn()
    shape_stats.Execute(seg)
    return shape_stats


def _calculate_intensity_stats(
    image: sitk.Image, seg: sitk.Image
) -> sitk.LabelIntensityStatisticsImageFilter:
    """Calculate intensity stats for a segmentation using the reference image
    Parameters
    ----------
    image : sitk.Image
        The reference image
    seg : sitk.Image
        The segmentation of the reference image
    Returns
    -------
    sitk.LabelIntensityStatisticsImageFilter
        The executed intensity stats
    """
    intensity_stats = sitk.LabelIntensityStatisticsImageFilter()
    intensity_stats.SetGlobalDefaultCoordinateTolerance(1e-5)
    intensity_stats.Execute(seg, image)
    return intensity_stats


def filter_segmentation(
    segmentation: sitk.Image,
    labels: str | list[str],
    label_map: dict[str, int],
    largest_connected_component: bool = False,
    remap: bool = False,
) -> sitk.Image:
    """Filter a segmentation to only include specified labels
    Parameters
    ----------
    segmentation : sitk.Image
        The segmentation to filter
    labels : str|list[str]
        The labels to keep in the segmentation
    label_map : dict[str, int]
        A mapping of structure names to label IDs
    remap : bool, optional
        If True, remap the labels indexed starting from 1, by default False
    Returns
    -------
    sitk.Image
        The filtered segmentation
    """
    filtered_segmentation = sitk.Image(segmentation.GetSize(), sitk.sitkUInt8)
    filtered_segmentation.CopyInformation(segmentation)
    if isinstance(labels, str):
        labels = [labels]
    for i, label in enumerate(labels, start=1):
        idx = label_map.get(label, None)
        if idx is not None:
            mask = sitk.BinaryThreshold(segmentation, idx, idx, 1, 0)
            if largest_connected_component:
                mask = get_largest_connected_component(mask)
            new_idx = i if remap else idx
            mask = mask * new_idx
            filtered_segmentation = sitk.Add(filtered_segmentation, mask)
    return filtered_segmentation


def get_largest_connected_component(binary_segmentation: sitk.Image) -> sitk.Image:
    """Get the largest connected component from a binary segmentation
    Parameters
    ----------
    binary_segmentation : sitk.Image
        The binary segmentation to get the largest connected component from
    Returns
    -------
    sitk.Image
        The largest connected component of the binary segmentation
    """
    cc_filter = sitk.ConnectedComponentImageFilter()
    labeled = cc_filter.Execute(binary_segmentation)
    relabel_filter = sitk.RelabelComponentImageFilter()
    relabeled = relabel_filter.Execute(labeled)
    largest_component = sitk.BinaryThreshold(relabeled, 1, 1, 1, 0)
    return largest_component


def get_regionprops(image) -> list:
    """Get region properties from a labeled image
    Parameters
    ----------
    image : np.ndarray
        The labeled image to get region properties from
    Returns
    -------
    list
        A list of region properties for each labeled region in the image
    """
    labeled_image = label(image)
    return regionprops(labeled_image)
