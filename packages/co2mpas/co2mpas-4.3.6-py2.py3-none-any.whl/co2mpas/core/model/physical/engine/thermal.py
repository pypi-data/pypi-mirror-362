# -*- coding: utf-8 -*-
#
# Copyright 2015-2025 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
"""
Functions and `dsp` model to model the engine coolant temperature.
"""
import numpy as np
import schedula as sh
from co2mpas.defaults import dfl
from numpy import arange, newaxis, hstack, prod, array
from scipy import linalg

dsp = sh.BlueDispatcher(
    name='thermal', description='Models the engine thermal behaviour.'
)


def _central_diff_weights(Np, ndiv=1):
    """
    Return weights for an Np-point central derivative.

    Assumes equally-spaced function points.

    If weights are in the vector w, then
    derivative is w[0] * f(x-ho*dx) + ... + w[-1] * f(x+h0*dx)

    Parameters
    ----------
    Np : int
        Number of points for the central derivative.
    ndiv : int, optional
        Number of divisions. Default is 1.

    Returns
    -------
    w : ndarray
        Weights for an Np-point central derivative. Its size is `Np`.

    Notes
    -----
    Can be inaccurate for a large number of points.

    Examples
    --------
    We can calculate a derivative value of a function.

    >>> def f(x):
    ...     return 2 * x**2 + 3
    >>> x = 3.0 # derivative point
    >>> h = 0.1 # differential step
    >>> Np = 3 # point number for central derivative
    >>> weights = _central_diff_weights(Np) # weights for first derivative
    >>> vals = [f(x + (i - Np/2) * h) for i in range(Np)]
    >>> sum(w * v for (w, v) in zip(weights, vals))/h
    11.79999999999998

    This value is close to the analytical solution:
    f'(x) = 4x, so f'(3) = 12

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Finite_difference

    """
    if Np < ndiv + 1:
        raise ValueError(
            "Number of points must be at least the derivative order + 1."
        )
    if Np % 2 == 0:
        raise ValueError("The number of points must be odd.")

    ho = Np >> 1
    x = arange(-ho, ho + 1.0)
    x = x[:, newaxis]
    X = x ** 0.0
    for k in range(1, Np):
        X = hstack([X, x ** k])
    w = prod(arange(1, ndiv + 1), axis=0) * linalg.inv(X)[ndiv]
    return w


def sci_misc_derivative(func, x0, dx=1.0, n=1, args=(), order=3):
    if order < n + 1:
        raise ValueError(
            "'order' (the number of points used to compute the derivative), "
            "must be at least the derivative order 'n' + 1."
        )
    if order % 2 == 0:
        raise ValueError(
            "'order' (the number of points used to compute the derivative) "
            "must be odd."
        )
    # pre-computed for n=1 and 2 and low-order for speed.
    if n == 1:
        if order == 3:
            weights = array([-1, 0, 1]) / 2.0
        elif order == 5:
            weights = array([1, -8, 0, 8, -1]) / 12.0
        elif order == 7:
            weights = array([-1, 9, -45, 0, 45, -9, 1]) / 60.0
        elif order == 9:
            weights = array([3, -32, 168, -672, 0, 672, -168, 32, -3]) / 840.0
        else:
            weights = _central_diff_weights(order, 1)
    elif n == 2:
        if order == 3:
            weights = array([1, -2.0, 1])
        elif order == 5:
            weights = array([-1, 16, -30, 16, -1]) / 12.0
        elif order == 7:
            weights = array([2, -27, 270, -490, 270, -27, 2]) / 180.0
        elif order == 9:
            weights = (
                    array([-9, 128, -1008, 8064, -14350, 8064, -1008, 128, -9])
                    / 5040.0
            )
        else:
            weights = _central_diff_weights(order, 2)
    else:
        weights = _central_diff_weights(order, n)
    val = 0.0
    ho = order >> 1
    for k in range(order):
        val += weights[k] * func(x0 + (k - ho) * dx, *args)
    return val / prod((dx,) * n, axis=0)


def _derivative(times, temp):
    import scipy.interpolate as sci_itp
    par = dfl.functions.calculate_engine_temperature_derivatives
    func = sci_itp.InterpolatedUnivariateSpline(times, temp, k=1)
    return sci_misc_derivative(func, times, dx=par.dx, order=par.order)


@sh.add_function(dsp, outputs=['engine_temperatures', 'temperature_shift'])
def calculate_engine_temperatures(
        engine_thermostat_temperature, times, engine_coolant_temperatures,
        on_engine):
    from statsmodels.nonparametric.smoothers_lowess import lowess
    from syncing.model import dsp
    par = dfl.functions.calculate_engine_temperature_derivatives
    temp = lowess(
        engine_coolant_temperatures, times, is_sorted=True,
        frac=par.tw * len(times) / (times[-1] - times[0]) ** 2, missing='none'
    )[:, 1].ravel()
    i = np.searchsorted(temp, engine_thermostat_temperature)
    shifts = dsp({
        'reference_name': 'ref', 'data': {
            'ref': {'x': times[:i], 'y': on_engine[:i]},
            'data': {'x': times[:i], 'y': _derivative(times[:i], temp[:i])}
        }
    }, ['shifts'])['shifts']
    if not (-20 <= shifts['data'] <= 30):
        shifts['data'] = 0
    sol = dsp({
        'shifts': shifts, 'reference_name': 'ref', 'data': {
            'ref': {'x': times},
            'data': {'x': times, 'y': temp}
        },
        'interpolation_method': 'cubic'
    })
    return sol['resampled']['data']['y'], shifts['data']


@sh.add_function(dsp, outputs=['engine_temperature_derivatives'])
def calculate_engine_temperature_derivatives(
        times, engine_temperatures):
    """
    Calculates the derivative of the engine temperature [°C/s].

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :return:
        Derivative of the engine temperature [°C/s].
    :rtype: numpy.array
    """
    return _derivative(times, engine_temperatures)


@sh.add_function(dsp, outputs=['max_engine_coolant_temperature'])
def identify_max_engine_coolant_temperature(engine_coolant_temperatures):
    """
    Identifies maximum engine coolant temperature [°C].

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :return:
        Maximum engine coolant temperature [°C].
    :rtype: float
    """
    return engine_coolant_temperatures.max()


@sh.add_function(dsp, outputs=['engine_temperature_regression_model'])
def calibrate_engine_temperature_regression_model(
        engine_thermostat_temperature, engine_temperatures, velocities,
        engine_temperature_derivatives, on_engine, engine_speeds_out,
        accelerations, after_treatment_warm_up_phases):
    """
    Calibrates an engine temperature regression model to predict engine
    temperatures.

    :param engine_thermostat_temperature:
        Engine thermostat temperature [°C].
    :type engine_thermostat_temperature: float

    :param on_engine:
        If the engine is on [-].
    :type on_engine: numpy.array

    :param engine_temperature_derivatives:
        Derivative of the engine temperature [°C/s].
    :type engine_temperature_derivatives: numpy.array

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :param velocities:
        Velocity [km/h].
    :type velocities: numpy.array

    :param engine_speeds_out:
        Engine speed [RPM].
    :type engine_speeds_out: numpy.array

    :param accelerations:
        Acceleration vector [m/s2].
    :type accelerations: numpy.array

    :return:
        The calibrated engine temperature regression model.
    :rtype: callable
    """
    from ._thermal import ThermalModel
    return ThermalModel(engine_thermostat_temperature).fit(
        engine_temperatures, engine_temperature_derivatives, on_engine,
        velocities, engine_speeds_out, accelerations,
        after_treatment_warm_up_phases
    )


@sh.add_function(dsp, outputs=['engine_temperatures'])
def predict_engine_temperatures(
        engine_temperature_regression_model, times, on_engine, velocities,
        engine_speeds_out, accelerations, after_treatment_warm_up_phases,
        initial_engine_temperature, max_engine_coolant_temperature):
    """
    Predicts the engine temperature [°C].

    :param engine_temperature_regression_model:
        Engine temperature regression engine_temperature_regression_model.
    :type engine_temperature_regression_model: callable

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param accelerations:
        Acceleration vector [m/s2].
    :type accelerations: numpy.array

    :param on_engine:
        If the engine is on [-].
    :type on_engine: numpy.array

    :param velocities:
        Velocity [km/h].
    :type velocities: numpy.array

    :param engine_speeds_out:
        Engine speed [RPM].
    :type engine_speeds_out: numpy.array

    :param initial_engine_temperature:
        Engine initial temperature [°C]
    :type initial_engine_temperature: float

    :param max_engine_coolant_temperature:
        Maximum engine coolant temperature [°C].
    :type max_engine_coolant_temperature: float

    :return:
        Engine coolant temperature vector [°C].
    :rtype: numpy.array
    """
    return engine_temperature_regression_model(
        times, on_engine, velocities, engine_speeds_out, accelerations,
        after_treatment_warm_up_phases, max_temp=max_engine_coolant_temperature,
        initial_temperature=initial_engine_temperature
    )


@sh.add_function(dsp, outputs=['engine_coolant_temperatures'])
def calculate_engine_coolant_temperatures(
        times, engine_temperatures, temperature_shift):
    from syncing.model import dsp
    sol = dsp({
        'shifts': {'data': -temperature_shift}, 'data': {
            'ref': {'x': times},
            'data': {'x': times, 'y': engine_temperatures}
        },
        'reference_name': 'ref', 'interpolation_method': 'cubic'
    })
    return sol['resampled']['data']['y']


# noinspection PyPep8Naming
@sh.add_function(
    dsp, inputs_kwargs=True, outputs=['engine_thermostat_temperature']
)
@sh.add_function(
    dsp, function_id='identify_engine_thermostat_temperature_v1',
    weight=sh.inf(11, 100), outputs=['engine_thermostat_temperature']
)
def identify_engine_thermostat_temperature(
        idle_engine_speed, times, accelerations, engine_coolant_temperatures,
        engine_speeds_out, gear_box_powers_out=None):
    """
    Identifies thermostat engine temperature and its limits [°C].

    :param idle_engine_speed:
        Engine speed idle median and std [RPM].
    :type idle_engine_speed: (float, float)

    :param times:
        Time vector [s].
    :type times: numpy.array

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :param gear_box_powers_out:
        Gear box power out vector [kW].
    :type gear_box_powers_out: numpy.array

    :param engine_speeds_out:
        Engine speed [RPM].
    :type engine_speeds_out: numpy.array

    :param accelerations:
        Acceleration vector [m/s2].
    :type accelerations: numpy.array

    :return:
        Engine thermostat temperature [°C].
    :rtype: float
    """
    args = engine_speeds_out, accelerations
    if gear_box_powers_out is not None:
        args += gear_box_powers_out,
    from ._thermal import _build_samples, _XGBRegressor
    X, Y = _build_samples(
        _derivative(times, engine_coolant_temperatures),
        engine_coolant_temperatures, *args
    )
    X, Y = np.column_stack((Y, X[:, 1:])), X[:, 0]
    t_max, t_min = Y.max(), Y.min()
    b = (t_max - (t_max - t_min) / 3) <= Y

    # noinspection PyArgumentEqualDefault
    model = _XGBRegressor(
        random_state=0, objective='reg:squarederror'
    ).fit(X[b], Y[b])
    ratio = np.arange(1, 1.5, 0.1) * idle_engine_speed[0]
    spl = np.zeros((len(ratio), X.shape[1]))
    spl[:, 1] = ratio
    # noinspection PyTypeChecker
    return float(np.median(model.predict(spl)))


@sh.add_function(dsp, outputs=['engine_thermostat_temperature_window'])
def identify_engine_thermostat_temperature_window(
        engine_thermostat_temperature, engine_coolant_temperatures):
    """
    Identifies thermostat engine temperature limits [°C].

    :param engine_thermostat_temperature:
        Engine thermostat temperature [°C].
    :type engine_thermostat_temperature: float

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :return:
        Thermostat engine temperature limits [°C].
    :rtype: float, float
    """

    thr = engine_thermostat_temperature
    # noinspection PyTypeChecker
    std = np.sqrt(np.mean((engine_coolant_temperatures - thr) ** 2))
    return thr - std, thr + std


@sh.add_function(dsp, outputs=['initial_engine_temperature'])
def identify_initial_engine_temperature(engine_temperatures):
    """
    Identifies initial engine temperature [°C].

    :param engine_coolant_temperatures:
        Engine coolant temperature vector [°C].
    :type engine_coolant_temperatures: numpy.array

    :return:
        Initial engine temperature [°C].
    :rtype: float
    """
    return float(engine_temperatures[0])
