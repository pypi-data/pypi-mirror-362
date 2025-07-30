# -*- coding: utf-8 -*-

__author__ = "ajshajib"

import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import make_lsq_spline
import matplotlib.pyplot as plt
from numpy.polynomial.chebyshev import chebfit
from numpy.polynomial.chebyshev import chebval


def polyval(coeffs, x):
    """Evaluate a polynomial at a point. The signature is the same as numpy.polyval.

    :param coeffs: Coefficients of the polynomial
    :type coeffs: np.ndarray
    :param x: Point to evaluate the polynomial
    :type x: float
    :return: Value of the polynomial at x
    :rtype: float
    """
    return chebval(x, coeffs)


def polyfit(x, y, deg, w=None):
    """Fit a polynomial to the data. The signature is the same as numpy.polyfit.

    :param x: x values
    :type x: np.ndarray
    :param y: y values
    :type y: np.ndarray
    :param deg: Degree of the polynomial
    :type deg: int
    :return: Coefficients of the polynomial
    :rtype: np.ndarray
    """
    return chebfit(x, y, deg, w=w)


class Util(object):

    @classmethod
    def find_extrema(
        cls, curve, init_peak_detection_proximity_threshold=50, is_peak=True
    ):
        """Find peaks or troughs of a curve.

        :param curve: 1D numpy array
        :type curve: np.ndarray
        :param init_peak_detection_proximity_threshold: Minimum distance between two
            extrema in pixels
        :type init_peak_detection_proximity_threshold: int
        :param is_peak: If True, find peaks, otherwise find troughs
        :type is_peak: bool
        :return: Indices of the extrema
        :rtype: np.ndarray
        """
        smooth_curve = cls.smooth_curve(curve)

        val = -2 if is_peak else 2
        extrema = np.where(np.diff(np.sign(np.diff(smooth_curve))) == val)[0]

        while np.any(np.diff(extrema) < init_peak_detection_proximity_threshold):
            close_index = np.where(
                np.diff(extrema) < init_peak_detection_proximity_threshold
            )[0][0]
            extrema = np.delete(extrema, close_index + 1)

        return extrema

    @staticmethod
    def smooth_curve(curve):
        """Smooth a curve using Savitzky-Golay filter.

        :param curve: 1D numpy array
        :type curve: np.ndarray
        :return: Smoothed curve
        :rtype: np.ndarray
        """
        return savgol_filter(savgol_filter(curve, 51, 3), 51, 3)

    @staticmethod
    def lighter_smooth_curve(curve):
        """Smooth a curve using Savitzky-Golay filter.

        :param curve: 1D numpy array
        :type curve: np.ndarray
        :return: Smoothed curve
        :rtype: np.ndarray
        """
        return savgol_filter(curve, 31, 3)

    @classmethod
    def find_init_peaks_troughs_mids(
        cls, curve, init_peak_detection_proximity_threshold=50
    ):
        """Find initial peaks, troughs, and midpoints of a curve.

        :param curve: 1D numpy array
        :type curve: np.ndarray
        :param init_peak_detection_proximity_threshold: Minimum distance between two
            extrema in pixels
        :type init_peak_detection_proximity_threshold: int
        :return: Peaks, troughs, and midpoints
        :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray]
        """
        peaks = cls.find_extrema(
            curve, init_peak_detection_proximity_threshold, is_peak=True
        )
        troughs = cls.find_extrema(
            curve, init_peak_detection_proximity_threshold, is_peak=False
        )
        all_extrema = []

        if peaks[0] < troughs[0]:
            for p, t in zip(peaks, troughs):
                all_extrema.append(p)
                all_extrema.append(t)
            if len(peaks) > len(troughs):
                all_extrema.append(peaks[-1])
        else:
            for p, t in zip(peaks, troughs):
                all_extrema.append(t)
                all_extrema.append(p)
            if len(troughs) > len(peaks):
                all_extrema.append(troughs[-1])

        all_extrema = np.array(all_extrema)

        # remove elements of peak and troughs that are not in all_extrema
        peaks = np.array([p for p in peaks if p in all_extrema])
        troughs = np.array([t for t in troughs if t in all_extrema])

        smooth_curve = cls.smooth_curve(curve)

        midpoints = []

        if peaks[0] < troughs[0]:
            iterator = [(a, b) for a, b in zip(peaks, troughs)] + [
                (a, b) for a, b in zip(troughs, peaks[1:])
            ]
        else:
            iterator = [(a, b) for a, b in zip(troughs, peaks)] + [
                (a, b) for a, b in zip(peaks, troughs[1:])
            ]

        for a, b in iterator:
            a, b = (b, a) if a > b else (a, b)

            a_value = smooth_curve[a]
            b_value = smooth_curve[b]
            mid_value = (a_value + b_value) / 2
            slice = smooth_curve[a:b]

            mid_index = np.argmin(np.abs(slice - mid_value))
            midpoints.append(a + mid_index)

        midpoints = np.array(midpoints)

        return peaks, troughs, midpoints, all_extrema

    @classmethod
    def get_init_params_polynomial(
        cls,
        curve,
        scaled_wavelengths,
        n_amplitude=2,
        n_offset=7,
        n_frequency=1,
        init_peak_detection_proximity_threshold=50,
        plot=False,
    ):
        """Get initial parameters for the curve fitting.

        :param curve: 1D numpy array
        :type curve: np.ndarray
        :param n_amplitude: Degree of the polynomial for the amplitude
        :type n_amplitude: int
        :param n_frequency: Degree of the polynomial for the frequency
        :type n_frequency: int
        :param n_offset: Degree of the polynomial for the offset
        :type n_offset: int
        :param plot: If True, plot the initial parameters
        :type plot: bool
        :return: Initial amplitude, frequency, offset, and phase
        :rtype: Tuple[np.ndarray, np.ndarray, np.ndarray, float]
        """
        peaks, troughs, midpoints, extrema = cls.find_init_peaks_troughs_mids(
            curve,
            init_peak_detection_proximity_threshold=init_peak_detection_proximity_threshold,
        )

        lighter_smooth_curve = cls.lighter_smooth_curve(curve)

        extrema_values = lighter_smooth_curve[extrema]
        extrema_sw = scaled_wavelengths[extrema]

        amplitude_params, offset_params, frequency_params, init_phi = (
            cls.fit_sine_function_to_extrema_polynomial(
                extrema_sw,
                extrema_values,
                np.array([True if i in peaks else False for i in extrema]),
                n_amplitude,
                n_offset,
                n_frequency,
                phi_0=None,
            )
        )

        if plot:
            plt.plot(scaled_wavelengths, curve, label="Input")
            plt.plot(scaled_wavelengths, lighter_smooth_curve, label="Smoothed")
            plt.scatter(
                scaled_wavelengths[peaks], lighter_smooth_curve[peaks], c="r", zorder=10
            )
            plt.scatter(
                scaled_wavelengths[troughs],
                lighter_smooth_curve[troughs],
                c="b",
                zorder=10,
            )
            plt.plot(
                scaled_wavelengths,
                1
                + polyval(amplitude_params, scaled_wavelengths)
                + polyval(offset_params, scaled_wavelengths),
                c="r",
                ls="--",
                label="Amplitude",
            )
            plt.plot(
                scaled_wavelengths,
                1 + polyval(offset_params, scaled_wavelengths),
                c="g",
                ls="--",
                label="Offset",
            )
            plt.plot(
                scaled_wavelengths,
                cls.fitted_sine_function_polynomial(
                    scaled_wavelengths,
                    amplitude_params,
                    offset_params,
                    frequency_params,
                    init_phi,
                ),
                c="k",
                ls="--",
                label="Fitted",
            )
            plt.legend()
            plt.show()

        return frequency_params, amplitude_params, offset_params, init_phi

    @classmethod
    def get_init_params_spline(
        cls,
        curve,
        scaled_wavelengths,
        n_amplitude=2,
        n_frequency=1,
        init_peak_detection_proximity_threshold=50,
        plot=False,
    ):
        """Get initial parameters for curve fitting using spline-based amplitude and
        frequency.

        :param curve: 1D numpy array of spectral values
        :param scaled_wavelengths: Corresponding wavelength values
        :param n_amplitude: Number of knots for amplitude spline
        :param n_frequency: Number of knots for frequency spline
        :param init_peak_detection_proximity_threshold: Minimum distance between extrema
            (in indices)
        :param plot: Whether to show diagnostic plots
        :return: Tuple containing (amplitude_spline, frequency_spline, phase_offset)
        """
        peaks, troughs, midpoints, extrema = cls.find_init_peaks_troughs_mids(
            curve,
            init_peak_detection_proximity_threshold=init_peak_detection_proximity_threshold,
        )

        lighter_smooth_curve = cls.lighter_smooth_curve(curve)

        extrema_values = lighter_smooth_curve[extrema]
        extrema_sw = scaled_wavelengths[extrema]

        amp_spline, frequency_spline, init_phi = (
            cls.fit_sine_function_to_extrema_spline(
                extrema_sw,
                extrema_values,
                np.array([True if i in peaks else False for i in extrema]),
                n_amplitude,
                n_frequency,
                phi_0=None,
            )
        )

        if plot:
            plt.plot(scaled_wavelengths, curve, label="Input")
            plt.plot(scaled_wavelengths, lighter_smooth_curve, label="Smoothed")
            plt.scatter(
                scaled_wavelengths[peaks], lighter_smooth_curve[peaks], c="r", zorder=10
            )
            plt.scatter(
                scaled_wavelengths[troughs],
                lighter_smooth_curve[troughs],
                c="b",
                zorder=10,
            )
            plt.plot(
                scaled_wavelengths,
                1 + amp_spline(scaled_wavelengths),
                c="r",
                ls="--",
                label="Amplitude",
            )
            plt.plot(
                scaled_wavelengths,
                cls.fitted_sine_function_spline(
                    scaled_wavelengths,
                    amp_spline,
                    frequency_spline,
                    init_phi,
                ),
                c="k",
                ls="--",
                label="Fitted",
            )
            plt.legend()
            plt.show()

            plt.plot(
                scaled_wavelengths,
                frequency_spline(scaled_wavelengths),
                label="Frequency",
            )
            plt.show()

        return amp_spline, frequency_spline, init_phi

    @classmethod
    def get_linear_freq_coeffs_from_extrema(cls, extrema, scaled_wavelengths):
        """Get the linear frequency coefficients from the extrema.

        :param extrema: Extrema
        :type extrema: np.ndarray
        :param scaled_wavelengths: Scaled wavelengths
        :type scaled_wavelengths: np.ndarray
        :return: Linear frequency coefficients
        :rtype: np.ndarray
        """
        A = []
        for i in range(len(extrema) - 1):
            A.append(
                [
                    scaled_wavelengths[extrema[i + 1]] ** 2
                    - scaled_wavelengths[extrema[i]] ** 2,
                    scaled_wavelengths[extrema[i + 1]] - scaled_wavelengths[extrema[i]],
                ]
            )
        A = np.array(A)
        b = np.ones(len(extrema) - 1) * 0.5
        print(A.shape, b.shape)
        x = np.linalg.lstsq(A, b)[0]

        return x

    @classmethod
    def fit_sine_function_to_extrema_polynomial(
        cls,
        extrema_positions,
        extrema_vals,
        is_peak,
        n_amplitude,
        n_offset,
        n_frequency,
        phi_0=None,
    ):
        """Fit a wiggly function to the peaks and troughs of a curve.

        :param extrema_positions: Positions of the extrema
        :type extrema_positions: np.ndarray
        :param extrema_vals: Values of the extrema
        :type extrema_vals: np.ndarray
        :param is_peak: If True, the extrema are peaks, otherwise they are troughs
        :type is_peak: np.ndarray
        :param n_amplitude: Degree of the polynomial for the amplitude
        :type n_amplitude: int
        :param n_offset: Degree of the polynomial for the offset
        :type n_offset: int
        :param n_frequency: Degree of the polynomial for the frequency
        :type n_frequency: int
        :param phi_0: Phase offset
        :type phi_0: float
        :return: amplitude coefficients, offset coefficients, frequency coefficients,
            phase offset
        """
        sorted_indices = np.argsort(extrema_positions)
        extrema_positions = extrema_positions[sorted_indices]
        extrema_values = extrema_vals[sorted_indices] - 1
        is_peak = is_peak[sorted_indices]

        # Fit amplitude A(x) and offset O(x) polynomials
        # y = A(x) + O(x) for peaks, y = -A(x) + O(x) for troughs
        A_matrix = []
        b = []
        for xi, yi, peak in zip(extrema_positions, extrema_values, is_peak):
            row_A = np.concatenate(
                [
                    [xi**k for k in range(n_amplitude + 1)],  # A(x) coefficients
                    [xi**k for k in range(n_offset + 1)],  # O(x) coefficients
                ]
            )
            if peak:
                A_matrix.append(
                    np.concatenate([row_A[: n_amplitude + 1], row_A[n_amplitude + 1 :]])
                )
            else:
                A_matrix.append(
                    np.concatenate(
                        [-row_A[: n_amplitude + 1], row_A[n_amplitude + 1 :]]
                    )
                )
            b.append(yi)

        # Solve least squares for amplitude and offset coefficients
        A_matrix = np.array(A_matrix)
        amplitude_offset_coeffs = np.linalg.lstsq(A_matrix, b, rcond=None)[0]
        amplitude_coeffs = amplitude_offset_coeffs[: n_amplitude + 1]
        offset_coeffs = amplitude_offset_coeffs[n_amplitude + 1 :]

        # Fit frequency polynomial F(x)
        A_freq = []
        b_freq = []
        for i in range(1, len(extrema_positions)):
            x_start = extrema_positions[i - 1]
            x_end = extrema_positions[i]
            # Phase difference required between points (π for peak-trough, 2π otherwise)
            delta_phase = np.pi if (is_peak[i - 1] != is_peak[i]) else 2 * np.pi
            # Equation: sum(F_k * (x_end^{k+1} - x_start^{k+1}) = delta_phase
            equation = [
                x_end ** (k + 1) - x_start ** (k + 1) for k in range(n_frequency + 1)
            ]
            A_freq.append(equation)
            b_freq.append(delta_phase)
        frequency_coeffs = np.linalg.lstsq(A_freq, b_freq, rcond=None)[0]

        # Compute phase offset phi_0
        x0 = extrema_positions[0]
        # Compute F(x0) * x0
        F_x0 = np.polyval(frequency_coeffs[::-1], x0)  # Reverse coeffs for polyval
        F_x0_x0 = F_x0 * x0

        # φ(x0) should be π/2 for peaks, 3π/2 for troughs
        target_phase = np.pi / 2 if is_peak[0] else 3 * np.pi / 2
        phi_0 = target_phase - F_x0_x0
        # target_phase = np.pi / 2 if is_peak[0] else 3 * np.pi / 2
        # phi0 = target_phase - 2 * np.pi * F_x0

        amplitude_coeffs = np.polynomial.chebyshev.poly2cheb(amplitude_coeffs)
        offset_coeffs = np.polynomial.chebyshev.poly2cheb(offset_coeffs)
        frequency_coeffs = np.polynomial.chebyshev.poly2cheb(frequency_coeffs)

        return amplitude_coeffs, offset_coeffs, frequency_coeffs, phi_0

    @classmethod
    def fit_sine_function_to_extrema_spline(
        cls,
        extrema_positions,
        extrema_vals,
        is_peak,
        n_amplitude,
        n_frequency,
        phi_0=None,
    ):
        """Fit a wiggly function to the peaks and troughs of a curve using splines for
        amplitude and frequency.

        :param extrema_positions: Positions of the extrema
        :type extrema_positions: np.ndarray
        :param extrema_vals: Values of the extrema
        :type extrema_vals: np.ndarray
        :param is_peak: If True, the extrema are peaks, otherwise they are troughs
        :type is_peak: np.ndarray
        :param n_amplitude: Degree of the polynomial for the amplitude
        :type n_amplitude: int
        :param n_offset: Degree of the polynomial for the offset
        :type n_offset: int
        :param n_frequency: Degree of the polynomial for the frequency
        :type n_frequency: int
        :param phi_0: Phase offset
        :type phi_0: float
        :return: amplitude spline, frequency spline, phase offset
        :rtype: tuple
        """
        # Sort extrema by position and prepare arrays
        sorted_indices = np.argsort(extrema_positions)
        extrema_positions = extrema_positions[sorted_indices]
        extrema_values = extrema_vals[sorted_indices] - 1
        is_peak = is_peak[sorted_indices]

        # Fit amplitude A(x) spline using least-squares spline fit
        abs_y = np.abs(extrema_values)

        # Create uniform knots for the spline
        knots = np.linspace(extrema_positions[0], extrema_positions[-1], n_amplitude)
        degree = 3  # Use cubic spline
        t = np.r_[
            [knots[0]] * degree, knots, [knots[-1]] * degree
        ]  # Extend knots for boundary conditions

        amp_spline = make_lsq_spline(extrema_positions, abs_y, t=t, k=degree)

        # Fit frequency polynomial F(x) by solving a linear system for phase differences
        A_freq = []
        b_freq = []
        for i in range(1, len(extrema_positions)):
            x_start = extrema_positions[i - 1]
            x_end = extrema_positions[i]
            # Phase difference required between points (π for peak-trough, 2π otherwise)
            delta_phase = np.pi if (is_peak[i - 1] != is_peak[i]) else 2 * np.pi
            # Build equation for frequency polynomial coefficients
            equation = [
                x_end ** (k + 1) - x_start ** (k + 1) for k in range(n_frequency + 1)
            ]
            A_freq.append(equation)
            b_freq.append(delta_phase)
        frequency_coeffs = np.linalg.lstsq(A_freq, b_freq, rcond=None)[0]

        # Compute phase offset phi_0 so that the first extremum matches the expected phase
        x0 = extrema_positions[0]
        # Compute F(x0) * x0
        F_x0 = np.polyval(frequency_coeffs[::-1], x0)  # Reverse coeffs for polyval
        F_x0_x0 = F_x0 * x0

        # φ(x0) should be π/2 for peaks, 3π/2 for troughs
        target_phase = np.pi / 2 if is_peak[0] else 3 * np.pi / 2
        phi_0 = target_phase - F_x0_x0

        # Build a spline for the frequency as a function of position
        frequency_at_extrema = np.polyval(frequency_coeffs[::-1], extrema_positions)
        knots = np.linspace(extrema_positions[0], extrema_positions[-1], n_frequency)
        t = np.r_[[knots[0]] * degree, knots, [knots[-1]] * degree]
        frequency_spline = make_lsq_spline(
            extrema_positions, frequency_at_extrema, t=t, k=degree
        )

        return amp_spline, frequency_spline, phi_0

    @classmethod
    def fitted_sine_function_polynomial(
        cls, xs, amplitude_coeffs, offset_coeffs, frequency_coeffs, phi_0
    ):
        """Evaluate the fitted sine function at x.

        :param xs: x values
        :type xs: np.ndarray
        :param amplitude_coeffs: Amplitude coefficients
        :type amplitude_coeffs: np.ndarray
        :param offset_coeffs: Offset coefficients
        :type offset_coeffs: np.ndarray
        :param frequency_coeffs: Frequency coefficients
        :type frequency_coeffs: np.ndarray
        :param phi_0: Phase offset
        :type phi_0: float
        :return: Fitted sine function values
        :rtype: np.ndarray
        """
        amp = polyval(amplitude_coeffs, xs)
        offset = polyval(offset_coeffs, xs)
        freq = polyval(frequency_coeffs, xs)

        return 1 + amp * np.sin(freq * xs + phi_0) + offset

    @classmethod
    def fitted_sine_function_spline(cls, xs, amp_spline, frequency_spline, phi_0):
        """Evaluate the fitted sine function at x.

        :param xs: x values
        :type xs: np.ndarray
        :param amplitude_coeffs: Amplitude coefficients
        :type amplitude_coeffs: np.ndarray
        :param offset_coeffs: Offset coefficients
        :type offset_coeffs: np.ndarray
        :param frequency_coeffs: Frequency coefficients
        :type frequency_coeffs: np.ndarray
        :param phi_0: Phase offset
        :type phi_0: float
        :return: Fitted sine function values
        :rtype: np.ndarray
        """
        amp = amp_spline(xs)
        freq = frequency_spline(xs)

        return 1 + amp * np.sin(freq * xs + phi_0)
