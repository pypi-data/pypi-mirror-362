import numpy as np
import pandas as pd


def add_unique_id(df):
    df_copy = df.copy()
    df_copy["ID_unico"] = [
        r"{}-{}".format(data["Id_nido"], data["Year"]) for _, data in df_copy.iterrows()
    ]
    return df_copy


def calculate_mass_diff_2(df):
    df_copy = df.copy()
    df_copy["Hora_dt"] = pd.to_datetime(df_copy["Hora"])
    df_copy["Fecha_dt"] = pd.to_datetime(df_copy["Fecha"] + " " + df_copy["Hora"])
    df_copy["diff_hours"] = df_copy["Fecha_dt"].diff(periods=1) / np.timedelta64(1, "h")
    df_copy["diff_weights"] = df_copy["Masa"].diff(periods=1)
    df_copy["mass_loss_rate"] = -df_copy["diff_weights"] / df_copy["diff_hours"]
    return df_copy


def calculate_mass_diff(df):
    df_copy = df.copy()
    df_copy["Hora_dt"] = pd.to_datetime(df_copy["Hora"])
    df_copy["diff_hours"] = df_copy["Hora_dt"].diff(periods=1).dt.seconds / 3600
    df_copy["diff_weights"] = df_copy["Masa"].diff(periods=1)
    df_copy["mass_loss_rate"] = -df_copy["diff_weights"] / df_copy["diff_hours"]
    return df_copy


def filter_post_meal_data(df):
    all_data = df.copy()
    meal_event_mask = all_data["diff_weights"] > 0
    meal_mass_diff_index = all_data[meal_event_mask].index
    post_meal_data = all_data.loc[meal_mass_diff_index + 1]
    index_to_drop = np.unique([*meal_mass_diff_index.values, *meal_mass_diff_index.values + 1])
    all_data = all_data.drop(index_to_drop)
    post_meal_data = post_meal_data[post_meal_data["diff_weights"] < 0]
    return all_data, post_meal_data


def mass_loss_lineal_model(chick_mass, alpha, beta):
    return alpha + beta * chick_mass


def calculate_mass_loss_no_feed(df_model, hours, chicks_mass):
    mass_loss_rate = mass_loss_lineal_model(chicks_mass, df_model["Alpha"][1], df_model["Beta"][1])
    return -mass_loss_rate * hours


def calculate_mass_loss_after_feed(df_model, hours, chicks_mass):
    mass_loss_rate = mass_loss_lineal_model(chicks_mass, df_model["Alpha"][0], df_model["Beta"][0])
    return -mass_loss_rate * hours


def evaluate_mass_loss_no_feed(df_data, df_model):
    df_copy = df_data.copy()
    df_copy["mass_loss_no_feed"] = calculate_mass_loss_no_feed(
        df_model, df_copy["diff_hours"], df_copy["Masa"]
    )
    return df_copy


def calculate_effective_mass_loss(df_data, df_model):
    df_copy = df_data.copy()
    df_copy["mass_loss_no_feed_half"] = calculate_mass_loss_no_feed(
        df_model, df_copy["diff_hours"] / 2, df_copy["Masa"]
    )
    df_copy["mass_loss_after_feed_half"] = calculate_mass_loss_after_feed(
        df_model, df_copy["diff_hours"] / 2, df_copy["Masa"]
    )
    df_copy["effective_mass_loss"] = (
        df_copy["mass_loss_no_feed_half"] + df_copy["mass_loss_after_feed_half"]
    )
    return df_copy


def filter_meal_events(df, df_model):
    df_copy = df.copy()
    df_copy = evaluate_mass_loss_no_feed(df_copy, df_model)
    mask = df_copy["diff_weights"] >= df_copy["mass_loss_no_feed"]
    return df_copy[mask]


def calculate_meal_size(df, df_model):
    df_copy = df.copy()
    df_copy = calculate_mass_diff_2(df_copy)
    df_copy = filter_meal_events(df_copy, df_model)
    df_copy = calculate_effective_mass_loss(df_copy, df_model)
    df_copy["feed_rate"] = df_copy["diff_weights"] - df_copy["effective_mass_loss"]
    return df_copy
