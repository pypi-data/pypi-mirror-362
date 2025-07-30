import numpy as np

from dataclasses import dataclass, field
from loguru import logger
from scipy.interpolate import splprep, splev


@dataclass
class Centerline:
    """
    Class representing a centerline for a vessel.
    """

    label: int
    vessel: str
    coordinates: np.ndarray
    _differences: np.ndarray = field(init=False, repr=False, default=None)
    _segment_lengths: np.ndarray = field(init=False, repr=False, default=None)
    _cumulative_lengths: np.ndarray = field(init=False, repr=False, default=None)
    _length: float = field(init=False, repr=False, default=None)
    u: np.ndarray = field(init=True, repr=False, default=None)
    tck: np.ndarray = field(init=True, repr=False, default=None)

    def __call__(self):
        """
        Return the centerline coordinates.
        """
        return self.coordinates

    def __len__(self):
        """
        Return the number of points in the centerline.
        """
        return len(self.coordinates)
    
    def len(self) -> int:
        return len(self.coordinates)
    
    @property
    def differences(self) -> float:
        if self._differences is None:
            self._differences = np.diff(self.coordinates, axis=0)
        return self._differences

    @property
    def segment_lengths(self) -> np.ndarray:
        if self._segment_lengths is None:
            self._segment_lengths = np.sqrt(np.sum(self.differences**2, axis=1))
        return self._segment_lengths

    @property
    def cumulative_lengths(self) -> np.ndarray:
        if self._cumulative_lengths is None:
            self._cumulative_lengths = np.concatenate(
                ([0], np.cumsum(self.segment_lengths))
            )
        return self._cumulative_lengths

    @property
    def length(self) -> float:
        # This is the length in voxel space - not in physical space. Need to adjust for spacing if physical length is desired.
        if self._length is None:
            self._length = self.cumulative_lengths[-1]
        return self._length

    def _reset_properties(self):
        """
        Reset all cached properties to force recalculation.
        """
        self._differences = None
        self._segment_lengths = None
        self._cumulative_lengths = None
        self._length = None

    def resample_with_spline(
        self, target_points: int, smoothing: float = 0.5, degree: int = 3
    ):
        """
        Resample centerline using B-spline interpolation for smoother results.

        Args:
            target_points: Number of points in resampled centerline
            smoothing: Smoothing factor (0 = interpolation, >0 = approximation)
            degree: Spline degree (1=linear, 2=quadratic, 3=cubic)
        """
        if target_points <= 0:
            raise ValueError("Target number of points must be greater than zero.")

        if len(self.coordinates) < degree + 1:
            raise ValueError(
                f"Need at least {degree + 1} points for degree {degree} spline"
            )

        # Prepare coordinates for splprep (transpose for per-dimension arrays)
        centerline = self.coordinates
        coords_t = centerline.T
        # Get the u parameter
        dists = np.linalg.norm(np.diff(centerline, axis=0), axis=1)
        u = np.concatenate(([0], np.cumsum(dists)))
        u /= u[-1]
        # Fit B-spline to the centerline
        # u is the parameter array, automatically computed based on chord length
        s = smoothing * len(centerline)
        tck, u = splprep(coords_t, u=u, s=s, k=degree, nest=-1)
        # Generate new parameter values for resampling
        u_new = np.linspace(0, 1, target_points)
        # Evaluate spline at new parameter values
        resampled_coords = splev(u_new, tck)
        resampled_coords = np.array(resampled_coords).T.round().astype(int)
        # Update the centerline coordinates
        self.coordinates = resampled_coords
        self.u = u_new
        self.tck = tck
        self._reset_properties()
        return self

    def calculate_tangent_vectors(self):
        """
        Calculate tangent vectors, normals, and binormals for the centerline.
        Returns:
            tangents: Tangent vectors at each point
            normals: Normal vectors at each point
            binormals: Binormal vectors at each point
        """
        if self.tck is None:
            raise ValueError(
                "Centerline must be resampled with a spline before calculating tangent vectors."
            )
        # Evaluate the spline to get the tangent vectors
        tangents = np.array(splev(self.u, self.tck, der=1)).T
        tangents /= np.linalg.norm(tangents, axis=1, keepdims=True)
        self.tangents = tangents
        return self
