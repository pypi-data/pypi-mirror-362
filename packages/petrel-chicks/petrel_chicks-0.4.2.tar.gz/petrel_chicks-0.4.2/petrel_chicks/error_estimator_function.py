#!/usr/bin/env python
# error_estimator_function uses the results from fit_logistic_grow_model to estimate the error.

from geci_plots import roundup, rounded_ticks_array
from lmfit import Model
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def calculate_time_days(data):
    days = []
    data_copy = data.copy()
    data_copy["Fecha"] = pd.to_datetime(data_copy["Fecha"])
    for i in range(len(data)):
        days.append((data_copy["Fecha"].iloc[i] - data_copy["Fecha"].iloc[0]).days)
    return np.array(days) + 1


def logistic_model(t, A, t0, k, n):
    return A * (1 + np.exp(-k * (t - t0))) ** (-1 / n)


def inverse_logistic_model(L, A, t0, k, n):
    t = t0 - ((1 / k) * np.log((A / L) ** n - 1))
    return t


initial_value = 1
minimum_value = 0


def initialize_logistic_model():
    model = Model(logistic_model)
    model.set_param_hint("A", value=initial_value, min=minimum_value)
    model.set_param_hint("t0", value=initial_value, min=minimum_value)
    model.set_param_hint("k", value=initial_value, min=minimum_value)
    model.set_param_hint("n", value=initial_value, min=minimum_value)
    params = model.make_params()
    return model, params


max_iterations = 20000


def fit_logistic_model(model, params, data, days, morphometric_variable):
    result = perform_fit(model, params, data, days, morphometric_variable)
    return results_logistic_parameters(result)


def perform_fit(model, params, data, days, morphometric_variable):
    return model.fit(
        data[morphometric_variable],
        params,
        t=days,
        method="least_squares",
        max_nfev=max_iterations,
    )


def results_logistic_parameters(fit_results):
    A = fit_results.params["A"].value
    t0 = fit_results.params["t0"].value
    k = fit_results.params["k"].value
    n = fit_results.params["n"].value
    return A, t0, k, n


def plot_morphometric_data(ax, df, morphometric_variable):
    ax.plot(
        df["Edad"],
        df[morphometric_variable],
        "-o",
    )
    return ax


def set_ticks_and_limits(ax, df, morphometric_variable):
    upper_limit = roundup(np.max(df[morphometric_variable]), 10)
    plt.xlim(0, 80)
    plt.ylim(0, upper_limit)
    rounded_ticks = rounded_ticks_array(upper_limit, 0)
    plt.yticks(rounded_ticks)
    ax.tick_params(axis="y", labelsize=20, labelrotation=90)
    ax.tick_params(axis="x", labelsize=20)
    return ax


def set_axis_labels(ax, morphometric_variable):
    if morphometric_variable == "Masa":
        ax.set_ylabel(f'{morphometric_variable.replace("_"," ")} (g)', fontsize=25, labelpad=10)
    else:
        ax.set_ylabel(f'{morphometric_variable.replace("_"," ")} (mm)', fontsize=25, labelpad=10)
    ax.set_xlabel("Días desde la eclosión", fontsize=25, labelpad=10)
