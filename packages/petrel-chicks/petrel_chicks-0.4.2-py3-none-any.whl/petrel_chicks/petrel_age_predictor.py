#!/usr/bin/env python
#
# petrel_age_predictor contiene clases para el filtrado de datos, ajuste del modelo y graficado.

from geci_plots import geci_plot
from geci_plots import fix_date
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import json
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import pandas as pd
import pickle
import io


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


class Cleaner_Morphometric:
    def __init__(self, data, features, observable):
        self.__features = features
        self.__observable = observable
        self.__variables = [*self.__observable, *self.__features]
        self.__select_subset(data)

    def __select_subset(self, morphometric_data):
        self.data_subset = morphometric_data[self.__variables].dropna()
        self.data_features = morphometric_data[self.__features].dropna()
        self.data_observable = morphometric_data[self.__observable].dropna()

    def train_test_split(self):
        self.features = self.data_subset[self.__features]
        self.observable = self.data_subset[self.__observable]
        X_train, X_test, y_train, y_test = train_test_split(
            self.features, self.observable, random_state=5
        )
        return X_train, X_test, y_train, y_test


class Fitter:
    def __init__(self, Cleaner_Morphometric):
        (
            self.X_train,
            self.X_test,
            self.y_train,
            self.y_test,
        ) = Cleaner_Morphometric.train_test_split()
        self.lineal_model = LinearRegression(normalize=True)
        self.exit_files_folder = "data/processed"

    def fit_model(self):
        self.lineal_model.fit(self.X_train, self.y_train)

    def ensure_processed(self):
        ensure_dir(self.exit_files_folder)

    def dump_model(self):
        self.ensure_processed()
        filename = "data/processed/trained_linear_model.pickle"
        pickle.dump(self.lineal_model, io.open(filename, "wb"))

    def load_model_pickle(self, model_path):
        self.lineal_model = pickle.load(open(model_path, "rb"))

    def predict_data(self, data):
        self.predictions = self.lineal_model.predict(data)

    def predict(self):
        self.predictions = self.lineal_model.predict(self.X_test)

    def calculate_absolute_error(self):
        self.absolute_error_in_days = abs(self.y_test.values - self.predictions)

    def calculate_results(self):
        self.fit_model()
        self.predict()
        self.calculate_absolute_error()
        self.predictions_dict = {
            "Edades": list(self.y_test.values.ravel()),
            "Predicciones": list(self.predictions.ravel()),
            "Error": list(self.absolute_error_in_days.ravel()),
        }
        self.linear_model_parameters = {
            "Alpha": self.lineal_model.intercept_.tolist(),
            "Beta": list(self.lineal_model.coef_.ravel()),
        }
        return self.predictions_dict, self.linear_model_parameters


class Predictions_and_Parameters:
    def __init__(self, predictions_dict, model_parameters_dict):
        self.predictions_dict = predictions_dict
        self.linear_model_parameters = model_parameters_dict
        self.exit_json_folder = "reports/non-tabular"

    def ensure_non_tabular(self):
        ensure_dir(self.exit_json_folder)

    def result_to_json(self, json_results_path):
        self.ensure_non_tabular()
        results_exit_dict = {**self.predictions_dict, **self.linear_model_parameters}
        with open(json_results_path, "w") as exit_file:
            json.dump(results_exit_dict, exit_file)

    def data_for_plot(self):
        results_df = pd.DataFrame(self.predictions_dict)
        grouped_results = results_df.groupby(by="Edades").mean()
        ages = grouped_results.index.to_list()
        prediction_days_diff = grouped_results["Error"].to_list()
        return ages, prediction_days_diff


class Plotter:
    def __init__(self, Predictions_and_Parameters):
        self.ages, self.prediction_days_diff = Predictions_and_Parameters.data_for_plot()
        self.fig, self.ax = geci_plot()
        self.exit_files_folder = "reports/figures"
        self.fontsize = 25

    def plot(self):
        self.ax.plot(self.ages, self.prediction_days_diff, "o")
        self.set_labels()
        self.set_ticks()
        self.set_limits()
        return self.ax

    def set_labels(self):
        self.ax.set_ylabel("Error (días)", fontsize=self.fontsize)
        self.ax.set_xlabel("Edad (días)", fontsize=self.fontsize)

    def set_ticks(self):
        self.ax.tick_params(axis="y", labelsize=self.fontsize, labelrotation=90)
        self.ax.tick_params(axis="x", labelsize=self.fontsize)
        self.ax.ticklabel_format(axis="y", style="sci")

    def set_limits(self):
        self.ax.set_ylim(0, 14)
        self.ax.set_xlim(0, 100)

    def ensure_dir(self):
        ensure_dir(self.exit_files_folder)

    def savefig(self, error_plot_path):
        self.ensure_dir()
        mpl.rcParams["savefig.transparent"] = True
        mpl.rcParams["savefig.dpi"] = 300
        plt.savefig(error_plot_path)
        return self.fig


def get_subset_morphometric_data(Cleaner_Morphometric, Predictor):
    data_subset = Cleaner_Morphometric.data_subset
    data_subset["age_predictions"] = Predictor.predictions
    data_subset["Fecha"] = data_subset.Fecha.apply(fix_date)
    data_subset["Fecha_dt"] = pd.to_datetime(data_subset["Fecha"], format="%d/%b/%Y")
    return data_subset


def correct_age(data_per_burrow):
    df_index = data_per_burrow.index.values
    for i in range(1, len(data_per_burrow)):
        data_per_burrow.loc[df_index[i], "age_predictions"] = (
            data_per_burrow["age_predictions"].iloc[i - 1]
            + data_per_burrow["Time_diff_days"].iloc[i].days
        )


def select_data_per_burrow(data_subset, id_petrel_chick):
    data_per_burrow = data_subset[data_subset.ID_unico == id_petrel_chick]
    data_per_burrow["Time_diff_days"] = data_per_burrow.Fecha_dt.diff(periods=1)
    return data_per_burrow


def update_with_age(data_modified, data_per_burrow):
    df_index = data_per_burrow.index.values
    for i in range(0, len(data_per_burrow)):
        data_modified.loc[df_index[i], "Edad"] = int(data_per_burrow["age_predictions"].iloc[i])


def fill_empty_age(updated_age_data):
    na_values_with_ffill = updated_age_data.groupby(
        [updated_age_data.ID_nido, updated_age_data.Year]
    ).Edad.ffill()
    increment_value = updated_age_data.groupby(
        [updated_age_data.ID_nido, updated_age_data.Year, updated_age_data.Edad.notnull().cumsum()]
    ).cumcount()
    updated_age_data["Edad"] = na_values_with_ffill + increment_value
    return updated_age_data


def bfill_empty_age(updated_age_data):
    pass
