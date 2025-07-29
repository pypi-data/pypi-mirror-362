"""Signal stability detection module."""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union, cast

import numpy as np
from numpy.typing import NDArray
from scipy import stats

try:
    import pywt  # type: ignore[import-not-found]
except ImportError:
    pywt = None


class StabilityMethod(Enum):
    """Available methods for stability detection."""

    DERIVATIVE = "derivative"  # Using signal derivative
    STATISTICAL = "statistical"  # Using statistical measures
    LINEAR_FIT = "linear_fit"  # Using linear regression
    ADAPTIVE = "adaptive"  # Using adaptive segmentation
    WAVELET = "wavelet"  # Using wavelet transform


class SignalStabilityDetector:
    """Class for detecting stable regions in signals."""

    def __init__(
        self,
        method: Union[StabilityMethod, str] = StabilityMethod.STATISTICAL,
        min_points: int = 100,
        **kwargs: Any,
    ):
        """
        Initialize stability detector.

        Args:
            method: Method to use for stability detection
            min_points: Minimum number of points for a stable region
            **kwargs: Additional parameters for specific methods
        """
        if isinstance(method, str):
            method = StabilityMethod(method)

        self.method = method
        self.min_points = min_points
        self.params = kwargs

    def find_stable_regions(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Find stable regions in signal.

        Args:
            signal: Signal array
            x_values: Optional x-axis values (time or other independent variable)
            **kwargs: Additional method-specific parameters

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        params = {**self.params, **kwargs}

        detection_methods = {
            StabilityMethod.DERIVATIVE: self._derivative_method,
            StabilityMethod.STATISTICAL: self._statistical_method,
            StabilityMethod.LINEAR_FIT: self._linear_fit_method,
            StabilityMethod.ADAPTIVE: self._adaptive_method,
            StabilityMethod.WAVELET: self._wavelet_method,
        }

        if self.method not in detection_methods:
            raise ValueError(f"Unknown stability detection method: {self.method}")

        return detection_methods[self.method](signal, x_values=x_values, **params)

    def _statistical_method(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Detect stable regions using statistical measures.

        Args:
            signal: Signal array
            x_values: Optional x-axis values (not used in this method)
            window_size: Size of the sliding window
            std_threshold: Maximum allowed standard deviation relative to signal range
            overlap: Fraction of overlap between windows (0 to 1)
            **kwargs: Additional parameters (ignored)

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        window_size = kwargs.get("window_size", 50)
        std_threshold = kwargs.get("std_threshold", 0.1)
        overlap = kwargs.get("overlap", 0.5)

        if len(signal) < window_size:
            return []

        # Calculate absolute threshold based on signal range
        signal_range = np.ptp(signal)
        if signal_range == 0:
            return [(0, len(signal))]
        abs_threshold = signal_range * std_threshold

        # Calculate window step size
        step = int(window_size * (1 - overlap))
        if step < 1:
            step = 1

        # Initialize variables
        stable_regions: List[Tuple[int, int]] = []
        n_windows = (len(signal) - window_size) // step + 1
        window_stats = np.zeros(n_windows)

        # Calculate standard deviation for each window
        for i in range(n_windows):
            start_idx = i * step
            end_idx = start_idx + window_size
            window_stats[i] = np.std(signal[start_idx:end_idx])

        # Find regions where std is below threshold
        stable_mask = window_stats < abs_threshold

        # Find continuous stable regions
        current_start: Optional[int] = None
        for i in range(len(stable_mask)):
            if stable_mask[i] and current_start is None:
                current_start = i * step
            elif (
                not stable_mask[i] or i == len(stable_mask) - 1
            ) and current_start is not None:
                end_idx = i * step + window_size
                if end_idx - current_start >= self.min_points:
                    # Refine region boundaries
                    region_signal = signal[current_start:end_idx]
                    if len(region_signal) > window_size:
                        local_stds = np.array(
                            [
                                np.std(region_signal[j : j + window_size])
                                for j in range(
                                    0, len(region_signal) - window_size, step
                                )
                            ]
                        )
                        # Find the most stable section within the region
                        best_idx = int(np.argmin(local_stds))
                        refined_start = current_start + best_idx * step
                        refined_end = min(refined_start + window_size, len(signal))
                        stable_regions.append((refined_start, refined_end))
                current_start = None

        return stable_regions

    def _linear_fit_method(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Detect stable regions using linear regression.

        Args:
            signal: Signal array
            x_values: Optional x-axis values
            window_size: Size of the sliding window
            r2_threshold: Minimum R² value for linear fit
            slope_tolerance: Maximum allowed relative change in slope between windows
            overlap: Fraction of overlap between windows (0 to 1)
            **kwargs: Additional parameters (ignored)

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        window_size = kwargs.get("window_size", 100)
        r2_threshold = kwargs.get("r2_threshold", 0.95)
        slope_tolerance = kwargs.get("slope_tolerance", 0.1)
        overlap = kwargs.get("overlap", 0.5)

        if len(signal) < window_size:
            return []

        x_data = x_values if x_values is not None else np.arange(len(signal))

        # Calculate window step size
        step = int(window_size * (1 - overlap))
        if step < 1:
            step = 1

        # Initialize variables
        stable_regions: List[Tuple[int, int]] = []
        n_windows = (len(signal) - window_size) // step + 1
        window_stats = np.zeros((n_windows, 3))  # [R², slope, intercept]

        # Calculate linear fit statistics for each window
        for i in range(n_windows):
            start_idx = i * step
            end_idx = start_idx + window_size
            window_x = x_data[start_idx:end_idx]
            window_y = signal[start_idx:end_idx]

            # Perform linear regression
            slope, intercept, r_value, _, _ = stats.linregress(window_x, window_y)
            window_stats[i] = [r_value**2, slope, intercept]

        # Find regions with good linear fit
        r2_mask = window_stats[:, 0] >= r2_threshold

        # Check for consistent slope
        slope_diffs = np.abs(np.diff(window_stats[:, 1]))
        mean_slope = np.mean(np.abs(window_stats[:, 1]))
        slope_mask = np.concatenate(
            (
                [True],
                slope_diffs
                <= slope_tolerance * (mean_slope if mean_slope > 0 else 1.0),
            )
        )

        # Combine criteria
        stable_mask = r2_mask & slope_mask

        # Find continuous stable regions
        current_start: Optional[int] = None
        for i in range(len(stable_mask)):
            if stable_mask[i] and current_start is None:
                current_start = i * step
            elif (
                not stable_mask[i] or i == len(stable_mask) - 1
            ) and current_start is not None:
                end_idx = i * step + window_size
                if end_idx - current_start >= self.min_points:
                    # Refine region boundaries
                    region_signal = signal[current_start:end_idx]
                    region_x = x_data[current_start:end_idx]

                    if len(region_signal) > window_size:
                        r2_values = []
                        for j in range(0, len(region_signal) - window_size, step):
                            sub_x = region_x[j : j + window_size]
                            sub_y = region_signal[j : j + window_size]
                            _, _, r_value, _, _ = stats.linregress(sub_x, sub_y)
                            r2_values.append(r_value**2)

                        if r2_values:
                            # Find the most linear section
                            best_idx = int(np.argmax(r2_values))
                            refined_start = current_start + best_idx * step
                            refined_end = min(refined_start + window_size, len(signal))
                            stable_regions.append((refined_start, refined_end))
                current_start = None

        return stable_regions

    def _adaptive_method(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Detect stable regions using adaptive segmentation.

        This method recursively divides the signal into segments until each segment
        meets stability criteria or minimum size is reached.

        Args:
            signal: Signal array
            x_values: Optional x-axis values
            min_segment_size: Minimum allowed segment size
            error_threshold: Maximum allowed error relative to linear fit
            max_depth: Maximum recursion depth
            **kwargs: Additional parameters

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        min_segment_size = kwargs.get("min_segment_size", 50)
        error_threshold = kwargs.get("error_threshold", 0.1)
        max_depth = kwargs.get("max_depth", 10)

        x_data = x_values if x_values is not None else np.arange(len(signal))

        stable_regions: List[Tuple[int, int]] = []

        def segment_error(start: int, end: int) -> float:
            """Calculate error between signal and linear fit."""
            if end - start < 2:
                return np.inf

            x = x_data[start:end]
            y = signal[start:end]
            signal_range = np.ptp(y)
            if signal_range == 0:
                return 0.0

            # Linear fit
            slope, intercept, _, _, _ = stats.linregress(x, y)
            y_fit = slope * x + intercept

            # Normalized error
            error = np.sqrt(np.mean((y - y_fit) ** 2)) / signal_range
            return float(error)

        def find_split_point(start: int, end: int) -> int:
            """Find optimal point to split segment."""
            if end - start < 3:
                return start + (end - start) // 2

            x = x_data[start:end]
            y = signal[start:end]

            # Linear fit
            slope, intercept, _, _, _ = stats.linregress(x, y)
            y_fit = slope * x + intercept

            # Find point of maximum deviation
            errors = np.abs(y - y_fit)
            return start + int(np.argmax(errors))

        def recursive_segment(start: int, end: int, depth: int = 0) -> None:
            """Recursively segment signal."""
            if depth >= max_depth or end - start < min_segment_size:
                return

            error = segment_error(start, end)

            if error < error_threshold:
                if end - start >= self.min_points:
                    stable_regions.append((start, end))
                return

            # Split segment
            split = find_split_point(start, end)
            if split > start and end > split:
                recursive_segment(start, split, depth + 1)
                recursive_segment(split, end, depth + 1)

        # Start recursive segmentation
        recursive_segment(0, len(signal))

        # Sort regions by start index
        stable_regions.sort(key=lambda x: x[0])
        return stable_regions

    def _wavelet_method(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Detect stable regions using wavelet transform.

        This method uses wavelet decomposition to identify regions with
        minimal high-frequency components.

        Args:
            signal: Signal array
            x_values: Optional x-axis values
            wavelet: Wavelet type to use
            level: Decomposition level
            threshold: Threshold for coefficient magnitudes
            **kwargs: Additional parameters

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        if pywt is None:
            raise ImportError(
                "pywt is required for wavelet method. Install with: pip install PyWavelets"
            )

        wavelet = kwargs.get("wavelet", "db4")
        level = kwargs.get("level", 3)
        threshold = kwargs.get("threshold", 0.1)

        if len(signal) < self.min_points:
            return []

        # Perform wavelet decomposition
        coeffs = pywt.wavedec(signal, wavelet, level=level)

        # Analyze detail coefficients
        detail_coeffs = coeffs[1:]

        # Calculate threshold for each level
        thresholds = []
        for detail in detail_coeffs:
            # Use signal range to normalize threshold
            detail_range = np.ptp(detail)
            thresholds.append(detail_range * threshold)

        # Initialize stability mask
        stability_mask = np.ones(len(signal), dtype=bool)

        # Analyze each level
        for i, (detail, thresh) in enumerate(zip(detail_coeffs, thresholds)):
            # Upsample detail coefficients to match signal length
            upsample_factor = 2 ** (i + 1)
            detail_upsampled = np.repeat(detail, upsample_factor)
            # Ensure length matches signal
            detail_upsampled = detail_upsampled[: len(signal)]

            # Update stability mask
            stability_mask &= np.abs(detail_upsampled) < thresh

        # Find continuous stable regions
        stable_regions: List[Tuple[int, int]] = []
        current_start: Optional[int] = None

        for i in range(len(stability_mask)):
            if stability_mask[i] and current_start is None:
                current_start = i
            elif (
                not stability_mask[i] or i == len(stability_mask) - 1
            ) and current_start is not None:
                end_idx = i
                if end_idx - current_start >= self.min_points:
                    stable_regions.append((current_start, end_idx))
                current_start = None

        return stable_regions

    def _derivative_method(
        self,
        signal: NDArray[np.float64],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> List[Tuple[int, int]]:
        """
        Detect stable regions using first and second derivatives.

        Args:
            signal: Signal array
            x_values: Optional x-axis values
            window_size: Size of the window for derivative calculation
            derivative_threshold: Maximum allowed first derivative
            second_derivative_threshold: Maximum allowed second derivative
            smooth_window: Window size for smoothing derivatives
            **kwargs: Additional parameters

        Returns:
            List of (start_idx, end_idx) tuples for stable regions
        """
        from .utilities import safe_savgol_filter

        window_size = kwargs.get("window_size", 20)
        derivative_threshold = kwargs.get("derivative_threshold", 0.1)
        second_derivative_threshold = kwargs.get("second_derivative_threshold", 0.05)
        smooth_window = kwargs.get("smooth_window", 7)

        if len(signal) < 2 * window_size:
            return []

        x_data = x_values if x_values is not None else np.arange(len(signal))

        # Smooth signal before derivative calculation
        smoothed_signal = signal
        if smooth_window > 1:
            smoothed_signal = safe_savgol_filter(signal, smooth_window, 3)

        # Calculate derivatives
        first_derivative = np.gradient(smoothed_signal, x_data)
        second_derivative = np.gradient(first_derivative, x_data)

        # Normalize thresholds by signal range
        signal_range = np.ptp(signal)
        norm_first_threshold = signal_range * derivative_threshold
        norm_second_threshold = signal_range * second_derivative_threshold

        # Create stability mask
        stable_mask = (np.abs(first_derivative) < norm_first_threshold) & (
            np.abs(second_derivative) < norm_second_threshold
        )

        # Find continuous regions
        stable_regions: List[Tuple[int, int]] = []
        current_start: Optional[int] = None

        for i in range(len(stable_mask)):
            if stable_mask[i] and current_start is None:
                current_start = i
            elif (
                not stable_mask[i] or i == len(stable_mask) - 1
            ) and current_start is not None:
                end_idx = i
                if end_idx - current_start >= self.min_points:
                    stable_regions.append((current_start, end_idx))
                current_start = None

        return stable_regions

    def _refine_derivative_region(
        self,
        signal: NDArray[np.float64],
        x_values: NDArray[np.float64],
        start_idx: int,
        end_idx: int,
        first_threshold: float,
        second_threshold: float,
    ) -> Tuple[int, int]:
        """Refine region boundaries using local derivative analysis."""
        # Calculate local derivatives
        segment = signal[start_idx:end_idx]
        x_segment = x_values[start_idx:end_idx]

        if len(segment) < 2:
            return start_idx, end_idx

        d1 = np.abs(np.gradient(segment, x_segment))
        d2 = np.abs(np.gradient(d1, x_segment))

        # Find most stable subsection
        stability_metric = d1 / first_threshold + d2 / second_threshold
        cumsum_metric = np.cumsum(stability_metric)

        # Find longest subsection with minimum cumulative change
        best_start, best_end = start_idx, end_idx
        min_length = self.min_points

        if len(cumsum_metric) > min_length:
            for i in range(len(cumsum_metric) - min_length):
                for j in range(i + min_length, len(cumsum_metric)):
                    section_metric = (cumsum_metric[j] - cumsum_metric[i]) / (j - i)
                    if section_metric < 1.0:  # normalized threshold
                        if j - i > best_end - best_start:
                            best_start = start_idx + i
                            best_end = start_idx + j

        return best_start, best_end

    def evaluate_stability(
        self,
        signal: NDArray[np.float64],
        region: Tuple[int, int],
        x_values: Optional[NDArray[np.float64]] = None,
        **kwargs: Any,
    ) -> Dict[str, float]:
        """
        Evaluate comprehensive stability metrics for a given region.

        Args:
            signal: Signal array
            region: (start_idx, end_idx) tuple defining the region
            x_values: Optional x-axis values
            **kwargs: Additional parameters

        Returns:
            Dictionary of stability metrics
        """
        start_idx, end_idx = region
        segment = signal[start_idx:end_idx]
        if len(segment) < 2:
            return {}

        x_data = x_values if x_values is not None else np.arange(len(signal))
        x_segment = x_data[start_idx:end_idx]

        # Basic statistics
        mean_val = float(np.mean(segment))
        std_val = float(np.std(segment))
        range_val = float(np.ptp(segment))

        # Trend analysis
        linearity = self._calculate_linearity(segment, x_segment)

        # Derivative-based metrics
        d1 = np.gradient(segment, x_segment)
        d2 = np.gradient(d1, x_segment)

        derivative_metrics = {
            "mean_d1": float(np.mean(np.abs(d1))),
            "std_d1": float(np.std(d1)),
            "mean_d2": float(np.mean(np.abs(d2))),
            "std_d2": float(np.std(d2)),
        }

        # Noise estimation
        noise_level = self._estimate_noise(segment)

        # Signal-to-noise ratio
        snr = float(range_val / noise_level if noise_level > 0 else np.inf)

        # Combine all metrics
        metrics = {
            "mean": mean_val,
            "std": std_val,
            "range": range_val,
            "linearity": linearity,
            "length": end_idx - start_idx,
            "noise_level": noise_level,
            "snr": snr,
            **derivative_metrics,
        }

        if range_val > 0:
            metrics["stability_score"] = self._calculate_stability_score(
                std_val / range_val,
                linearity,
                derivative_metrics["std_d1"] / range_val,
                derivative_metrics["std_d2"] / range_val,
                snr,
            )
        else:
            metrics["stability_score"] = 1.0

        return metrics

    def _calculate_linearity(
        self,
        signal: NDArray[np.float64],
        x_values: NDArray[np.number[Any]],
    ) -> float:
        """
        Calculate comprehensive linearity metric.

        Uses both R² and residual analysis for a more robust measure.
        """
        if len(signal) < 2:
            return 1.0

        # Linear regression
        slope, intercept, r_value, _, _ = stats.linregress(x_values, signal)
        r2 = float(r_value**2)

        # Residual analysis
        y_pred = slope * x_values + intercept
        residuals = signal - y_pred
        residual_std = np.std(residuals)
        signal_std = np.std(signal)

        if signal_std == 0:
            return 1.0

        # Combine metrics
        # Weight R² more heavily but consider residual distribution
        linearity = 0.7 * r2 + 0.3 * (1 - residual_std / signal_std)

        return float(np.clip(linearity, 0, 1))

    def _estimate_noise(
        self, signal: NDArray[np.float64], window_size: int = 5
    ) -> float:
        """
        Estimate noise level using median absolute deviation of differences.

        More robust than simple standard deviation.
        """
        if len(signal) < 2:
            return 0.0

        # Use differences to remove trend
        differences = np.diff(signal)

        if len(differences) == 0:
            return 0.0

        # Median absolute deviation (MAD) is more robust to outliers
        mad = np.median(np.abs(differences - np.median(differences)))

        # Convert MAD to standard deviation estimate
        noise_level = mad * 1.4826  # factor for normal distribution

        return float(noise_level)

    def _calculate_stability_score(
        self,
        normalized_std: float,
        linearity: float,
        normalized_d1_std: float,
        normalized_d2_std: float,
        snr: float,
    ) -> float:
        """
        Calculate overall stability score combining multiple metrics.

        Returns a score between 0 (unstable) and 1 (very stable).
        """
        # Weight the different components
        weights = {"std": 0.25, "linearity": 0.25, "d1": 0.2, "d2": 0.15, "snr": 0.15}

        # Transform SNR to 0-1 scale
        snr_score = 1 - np.exp(-snr / 10) if np.isfinite(snr) else 1.0

        # Calculate weighted score
        score = (
            weights["std"] * (1 - normalized_std)
            + weights["linearity"] * linearity
            + weights["d1"] * (1 - normalized_d1_std)
            + weights["d2"] * (1 - normalized_d2_std)
            + weights["snr"] * snr_score
        )

        return float(np.clip(score, 0, 1))
