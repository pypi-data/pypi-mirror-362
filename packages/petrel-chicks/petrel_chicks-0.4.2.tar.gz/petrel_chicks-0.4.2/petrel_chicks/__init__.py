"A module to petrel_chicks"

__version__ = "0.4.2"
from .cli import *  # noqa
from .calculate_mass_loss_rates import *  # noqa
from .error_estimator_function import *  # noqa
from .filter_per_season import *  # noqa
from .fit_model_for_peak_mass import *  # noqa
from .petrel_age_predictor import *  # noqa
from .plot_peak_mass_model import (  # noqa
    _plot_peak_mass_model_and_data,
    _plot_peak_mass_model_and_data_by_season,
    get_fitted_points,
)
