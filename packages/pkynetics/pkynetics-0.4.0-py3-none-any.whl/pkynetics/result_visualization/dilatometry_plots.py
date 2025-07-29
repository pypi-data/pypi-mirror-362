from typing import Dict

import matplotlib.pyplot as plt
import numpy as np


def plot_raw_and_smoothed(
    ax: plt.Axes,
    temperature: np.ndarray,
    strain: np.ndarray,
    smooth_strain: np.ndarray,
    method: str,
) -> None:
    """
    Plot raw and smoothed dilatometry data.

    Args:
        ax: Matplotlib axes object
        temperature: Temperature data array
        strain: Raw strain data array
        smooth_strain: Smoothed strain data array
        method: Analysis method name for plot title
    """
    ax.plot(temperature, strain, label="Raw data", alpha=0.5)
    ax.plot(temperature, smooth_strain, label="Smoothed data", color="r")
    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Relative Change")
    ax.set_title(f"Raw and Smoothed Dilatometry Data ({method.capitalize()} Method)")
    ax.legend()
    ax.grid(True)


def plot_transformation_points(
    ax: plt.Axes, temperature: np.ndarray, smooth_strain: np.ndarray, results: Dict
) -> None:
    """
    Plot strain data with transformation points and extrapolations.

    Args:
        ax: Matplotlib axes object
        temperature: Temperature data array
        smooth_strain: Smoothed strain data array
        results: Dictionary containing analysis results
    """
    ax.plot(temperature, smooth_strain, label="Strain")
    ax.plot(
        temperature, results["before_extrapolation"], "--", label="Before extrapolation"
    )
    ax.plot(
        temperature, results["after_extrapolation"], "--", label="After extrapolation"
    )

    points = {
        "Start": ("start_temperature", "green"),
        "End": ("end_temperature", "red"),
        "Mid": ("mid_temperature", "blue"),
    }

    y_range = ax.get_ylim()
    text_y_positions = np.linspace(y_range[0], y_range[1], len(points) + 2)[1:-1]

    for (label, (temp_key, color)), y_pos in zip(points.items(), text_y_positions):
        temp = results[temp_key]
        ax.axvline(temp, color=color, linestyle="--", label=label)
        ax.annotate(
            f"{label}: {temp:.1f}°C",
            xy=(temp, y_pos),
            xytext=(10, 0),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7),
            ha="left",
            va="center",
        )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Relative Change")
    ax.set_title("Dilatometry Curve with Transformation Points and Extrapolations")
    ax.legend()
    ax.grid(True)


def plot_lever_rule(
    ax: plt.Axes, temperature: np.ndarray, smooth_strain: np.ndarray, results: Dict
) -> None:
    """
    Plot lever rule representation with correct mid-point positioning.

    Args:
        ax: Matplotlib axes object
        temperature: Temperature data array
        smooth_strain: Smoothed strain data array
        results: Dictionary containing analysis results
    """
    is_cooling = results.get("is_cooling", False)

    # Plot main data
    ax.plot(temperature, smooth_strain, label="Strain")
    ax.plot(
        temperature, results["before_extrapolation"], "--", label="Before extrapolation"
    )
    ax.plot(
        temperature, results["after_extrapolation"], "--", label="After extrapolation"
    )

    # Get mid-point temperature
    mid_temp = results["mid_temperature"]

    # Find actual strain value at mid temperature using interpolation
    # Use numpy's interp function which handles both ascending and descending x values
    indices = np.argsort(temperature)
    sorted_temp = temperature[indices]
    sorted_strain = smooth_strain[indices]
    mid_strain = np.interp(mid_temp, sorted_temp, sorted_strain)

    # Calculate the extrapolated values at mid-point
    before_extrap_at_mid = np.interp(
        mid_temp, sorted_temp, results["before_extrapolation"][indices]
    )

    after_extrap_at_mid = np.interp(
        mid_temp, sorted_temp, results["after_extrapolation"][indices]
    )

    # Draw vertical lever line
    ax.plot(
        [mid_temp, mid_temp],
        [before_extrap_at_mid, after_extrap_at_mid],
        "k-",
        label="Lever",
    )

    # Add mid-point marker on the actual curve (not between extrapolations)
    ax.plot(mid_temp, mid_strain, "ro", label="Mid point")

    # Adjust text position based on cooling/heating direction
    if is_cooling:
        text_offset = (-10, 10)  # Place text to the left for cooling
        ha_align = "right"
    else:
        text_offset = (10, 10)  # Place text to the right for heating
        ha_align = "left"

    ax.annotate(
        f"Mid point: {mid_temp:.1f}°C",
        xy=(mid_temp, mid_strain),  # Anchor to actual strain value
        xytext=text_offset,
        textcoords="offset points",
        bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7),
        ha=ha_align,
    )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Relative Change")
    ax.set_title("Lever Rule Representation")
    ax.legend()
    ax.grid(True)


def plot_transformed_fraction(
    ax: plt.Axes, temperature: np.ndarray, results: Dict
) -> None:
    """
    Plot transformed fraction vs temperature.

    Args:
        ax: Matplotlib axes object
        temperature: Temperature data array
        results: Dictionary containing analysis results
    """
    is_cooling = results.get("is_cooling", False)
    transformed_fraction = results["transformed_fraction"]

    ax.plot(temperature, transformed_fraction, label="Transformed Fraction")

    # Adjust points based on direction
    start_fraction = 1.0 if is_cooling else 0.0
    end_fraction = 0.0 if is_cooling else 1.0

    points = {
        "Start": ("start_temperature", "green", start_fraction),
        "Mid": ("mid_temperature", "blue", 0.5),
        "End": ("end_temperature", "red", end_fraction),
    }

    for label, (temp_key, color, fraction) in points.items():
        temp = results[temp_key]
        ax.axvline(temp, color=color, linestyle="--", label=f"{label}")
        ax.plot(temp, fraction, "o", color=color)
        ax.annotate(
            f"{label}: {temp:.1f}°C\n{fraction * 100:.1f}%",
            xy=(temp, fraction),
            xytext=(10, 0),
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="white", alpha=0.7),
        )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Transformed Fraction")
    ax.set_title("Transformed Fraction vs Temperature")
    ax.set_ylim(-0.1, 1.1)
    ax.legend()
    ax.grid(True)


def plot_dilatometry_analysis(
    temperature: np.ndarray,
    strain: np.ndarray,
    smooth_strain: np.ndarray,
    results: Dict,
    method: str,
) -> plt.Figure:
    """
    Create complete visualization of dilatometry analysis.

    Args:
        temperature: Temperature data array
        strain: Raw strain data array
        smooth_strain: Smoothed strain data array
        results: Dictionary containing analysis results
        method: Analysis method name

    Returns:
        matplotlib.figure.Figure: Complete figure with all plots
    """
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 20))

    plot_raw_and_smoothed(ax1, temperature, strain, smooth_strain, method)
    plot_transformation_points(ax2, temperature, smooth_strain, results)
    plot_lever_rule(ax3, temperature, smooth_strain, results)
    plot_transformed_fraction(ax4, temperature, results)

    plt.tight_layout()
    return fig
