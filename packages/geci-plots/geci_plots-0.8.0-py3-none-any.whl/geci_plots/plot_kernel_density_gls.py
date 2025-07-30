from geci_plots import np, plt, roundup, rounddown
from geoambiental import PointArray, get_kernel_density_geographic
import matplotlib.pyplot as mpl
from matplotlib.colors import ListedColormap
import matplotlib.ticker as ticker


from PIL import Image

import pandas as pd
import geopandas as gpd


def adapt_geographic_data(gls_data_path):
    gls_data = pd.read_csv(gls_data_path)
    gls_data.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}, inplace=True)
    return gls_data


def _plot_kernel_density_and_points(
    gls_data, global_shapefile_data_path, path_rose_wind, selected_contour, bandwidth
):
    gls_data_translated = translate_positive_longitudes(gls_data)

    fig, ax = plt.subplots(figsize=(14.3, 10.4))
    format_plot(ax, gls_data_translated)
    plot_global_politic_division(global_shapefile_data_path, ax)
    plot_geographic_points(gls_data_translated)
    plot_kernel_contour(gls_data_translated, selected_contour, bandwidth)
    plot_windrose(path_rose_wind, fig)
    return ax


def _plot_kernel_density(
    gls_data, global_shapefile_data_path, path_rose_wind, selected_contour, bandwidth
):
    gls_data_translated = translate_positive_longitudes(gls_data)

    fig, ax = plt.subplots(figsize=(14.3, 10.4))
    format_plot(ax, gls_data_translated)
    plot_global_politic_division(global_shapefile_data_path, ax)
    plot_kernel_contour(gls_data_translated, selected_contour, bandwidth)
    plot_windrose(path_rose_wind, fig)
    plt.ylim(20, 40)
    plt.xlim(-130, -110)
    return ax


def _plot_geographic_points(gls_data, global_shapefile_data_path, path_rose_wind):
    gls_data_translated = translate_positive_longitudes(gls_data)

    fig, ax = plt.subplots(figsize=(14.3, 10.4))
    format_plot(ax, gls_data_translated)
    plot_global_politic_division(global_shapefile_data_path, ax)
    plot_geographic_points(gls_data_translated)
    plot_windrose(path_rose_wind, fig)
    return ax


def _plot_geographic_points_by_trip(gls_data, global_shapefile_data_path, path_rose_wind):
    gls_data_translated = translate_positive_longitudes(gls_data)

    fig, ax = plt.subplots(figsize=(14.3, 10.4))
    format_plot(ax, gls_data_translated)
    plot_global_politic_division(global_shapefile_data_path, ax)

    for label, df in gls_data_translated.groupby("tripID"):
        plt.plot(df["longitude"], df["latitude"], ".", markersize=2, label=label)
    plot_windrose(path_rose_wind, fig)
    return ax


def _plot_geographic_points_by_vessel(gls_data, global_shapefile_data_path, path_rose_wind):
    gls_data_translated = translate_positive_longitudes(gls_data)

    fig, ax = plt.subplots(figsize=(14.3, 10.4))
    format_plot(ax, gls_data_translated)
    plot_global_politic_division(global_shapefile_data_path, ax)

    for label, df in gls_data_translated.groupby("RNP"):
        plt.plot(df["longitude"], df["latitude"], ".", markersize=2, label=label)
    plot_windrose(path_rose_wind, fig)
    plt.ylim(-10, 40)
    plt.xlim(-150, -80)
    return ax


def translate_positive_longitudes(gls_data):
    mask_datos_trand = gls_data.longitude > 0
    gls_data.loc[mask_datos_trand, "longitude"] = gls_data[mask_datos_trand]["longitude"] - 360
    return gls_data


def plot_geographic_points(gls_data):
    plt.plot(gls_data["longitude"], gls_data["latitude"], ".b", markersize=3)


def plot_kernel_contour(gls_data, selected_contour, bandwidth):
    kernel = get_kernel_density(gls_data, bandwidth)
    normalized_kernel = np.array(kernel[2]) / np.nanmax(kernel[2])
    if selected_contour == "All_contours":
        hot = mpl.colormaps["hot_r"]
        new_hot = hot(np.linspace(0, 1, 256))
        new_hot[0:15, 3] = 0
        new_hot[15:-1, 3] = 0.3
        new_hor_r = ListedColormap(new_hot)
        plt.contourf(kernel[0], kernel[1], normalized_kernel, 100, cmap=new_hor_r)
    elif selected_contour == "50_contour":
        colors = [
            (0.1, 0.1, 0.5, 0),
            (1, 0, 0, 0.5),
            (1, 1, 1, 1),
        ]
        plt.contourf(
            kernel[0],
            kernel[1],
            normalized_kernel,
            [0, np.max(normalized_kernel) / 2, np.max(normalized_kernel)],
            colors=colors,
        )


def format_plot(ax, track_data):
    sea_color = "#E6FFFF"
    plt.gca().set_facecolor(sea_color)
    limits = get_limits(track_data)
    plt.xlim(limits["x_min"], limits["x_max"])
    plt.ylim(limits["y_min"], limits["y_max"])
    plt.yticks(size=20)
    plt.xticks(size=20)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d°"))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d°"))


def get_limits(track_data):
    multiplier = 10
    y_max = roundup(track_data["latitude"].max(), multiplier)
    y_min = rounddown(track_data["latitude"].min(), multiplier)
    x_max = roundup(track_data["longitude"].max(), multiplier)
    x_min = rounddown(track_data["longitude"].min(), multiplier)
    return {"y_max": y_max, "y_min": y_min, "x_max": x_max, "x_min": x_min}


def get_kernel_density(gls_data, bandwidth):
    point_array = PointArray(gls_data["latitude"], gls_data["longitude"])
    kernel = get_kernel_density_geographic(point_array, bandwidth)
    return kernel


def plot_windrose(path_rose_wind, fig):
    rose_wind = Image.open(path_rose_wind)
    width, height = rose_wind.size
    rescale_factor = 4
    new_size = (round(width / rescale_factor), round(height / rescale_factor))
    resized_rose_wind = rose_wind.resize(new_size)
    img_x = 1150
    img_y = 730
    fig.figimage(resized_rose_wind, img_x, img_y, origin="upper", zorder=100)


def plot_global_politic_division(global_shapefile_data_path, ax):
    global_shapefile = gpd.read_file(global_shapefile_data_path)
    global_shapefile_translated = global_shapefile.translate(-360)
    land_color = "#FFFAE6"
    global_shapefile.plot(ax=ax, color=land_color, edgecolor="black", linewidth=0.3)
    global_shapefile_translated.plot(ax=ax, color=land_color, edgecolor="black", linewidth=0.3)
