import matplotlib.pyplot as plt
import pandas as pd
import typer

from petrel_chicks.plot_peak_mass_model import (
    _plot_peak_mass_model_and_data_by_season,
    _plot_all_peak_mass_models,
)
import petrel_chicks as pc


cli = typer.Typer()


@cli.command()
def plot_all_peak_mass_models(
    data_path: str = typer.Option(help="Input file path"),
    font_name: str = typer.Option("STIXGeneral"),
    output_path: str = typer.Option(help="Output file path"),
):
    df = pd.read_csv(data_path)
    _plot_all_peak_mass_models(df, font_family=font_name)
    plt.savefig(output_path, transparent=True, dpi=600)


@cli.command()
def plot_peak_mass_model(
    data_path: str = typer.Option(help="Input file path"),
    season: int = typer.Option(help="Season"),
    output_path: str = typer.Option(help="Output file path"),
):
    data = pd.read_csv(data_path)
    _plot_peak_mass_model_and_data_by_season(data, season)
    plt.savefig(output_path, transparent=True)
    plt.clf()


@cli.command()
def version():
    print(pc.__version__)
