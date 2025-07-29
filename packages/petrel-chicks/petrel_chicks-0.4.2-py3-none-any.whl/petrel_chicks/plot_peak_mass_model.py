import geci_plots as gp
import matplotlib.pyplot as plt
import numpy as np

from petrel_chicks.fit_model_for_peak_mass import fit_model_mass_vs_age, quadratic_function
from petrel_chicks.filter_per_season import add_anio_column


def _plot_all_peak_mass_models(df):
    _, ax = gp.geci_plot()
    plotter = _Plotter_model_for_all_seasons(df)
    plotter.plot_model_for_all_seasons()
    plotter.setup_chicks_mass_vs_age_figure()
    plotter.write_season_legends()
    return ax


class _Plotter_model_for_all_seasons:
    def __init__(self, df):
        self.df = df
        self.fontsize = 20

    def plot_model_for_all_seasons(self):
        for season in self.all_season:
            filtered_data = self.df[self.df.Year == season]
            age, predicted_mass = get_fitted_points(filtered_data)
            plt.plot(age, predicted_mass)

    def write_season_legends(self) -> None:
        legends = [f"Season {season}" for season in self.all_season]
        plt.legend(legends, fontsize=18)

    @property
    def all_season(self):
        return self.df.Year.unique()

    def setup_chicks_mass_vs_age_figure(self) -> None:
        _setup_chicks_mass_vs_age_figure(self.fontsize)


def _plot_peak_mass_model_and_data_by_season(df, season):
    df_with_year = add_anio_column(df)
    filtered_data = df_with_year[df_with_year.Anio == season]
    return _plot_peak_mass_model_and_data(filtered_data)


def _plot_peak_mass_model_and_data(df):
    _, ax = gp.geci_plot()
    fontsize = 20

    plt.scatter(df.Edad, df.Masa, alpha=0.5)
    age, predicted_mass = get_fitted_points(df)

    plt.plot(age, predicted_mass, color="r")
    _setup_chicks_mass_vs_age_figure(fontsize)
    plt.legend(["Measured bird mass", "Fitted model"])
    return ax


def _setup_chicks_mass_vs_age_figure(fontsize: int) -> None:
    plt.ylabel("Mass $\\left( g \\right)$", fontsize=fontsize)
    plt.xlabel("Chick age $\\left( days \\right)$", fontsize=fontsize)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)


def get_fitted_mass(df, age):
    parameters, _ = fit_model_mass_vs_age(df)
    return [quadratic_function(x, *parameters) for x in age]


def get_fitted_points(df):
    age = np.linspace(df.Edad.min(), df.Edad.max(), 1000)
    predicted_mass = get_fitted_mass(df, age)
    return age, predicted_mass
