from geci_plots.plot_kernel_density_gls import (
    _plot_geographic_points,
    _plot_geographic_points_by_trip,
    _plot_geographic_points_by_vessel,
    _plot_kernel_density,
    _plot_kernel_density_and_points,
    adapt_geographic_data,
)
from geci_plots.boxplots import create_box_plot, create_box_plot_data_from_columns
import geci_plots as gp
import matplotlib.pyplot as plt
import pandas as pd
import typer

cli = typer.Typer()


@cli.command()
def plot_kernel_density_and_points(
    geographic_data_path: str = typer.Option(),
    global_shapefile_data_path: str = typer.Option(),
    path_rose_wind: str = typer.Option(),
    selected_contour: str = typer.Option(),
    result_map_path: str = typer.Option(),
    bandwidth: float = typer.Option(),
):
    geographic_data = adapt_geographic_data(geographic_data_path)
    _plot_kernel_density_and_points(
        geographic_data, global_shapefile_data_path, path_rose_wind, selected_contour, bandwidth
    )
    plt.savefig(result_map_path)


@cli.command()
def plot_kernel_density(
    geographic_data_path: str = typer.Option(),
    global_shapefile_data_path: str = typer.Option(),
    path_rose_wind: str = typer.Option(),
    selected_contour: str = typer.Option(),
    result_map_path: str = typer.Option(),
    bandwidth: float = typer.Option(),
):
    geographic_data = adapt_geographic_data(geographic_data_path)
    _plot_kernel_density(
        geographic_data, global_shapefile_data_path, path_rose_wind, selected_contour, bandwidth
    )
    plt.savefig(result_map_path)


@cli.command()
def plot_geographic_points(
    geographic_data_path: str = typer.Option(),
    global_shapefile_data_path: str = typer.Option(),
    path_rose_wind: str = typer.Option(),
    result_map_path: str = typer.Option(),
):
    geographic_data = adapt_geographic_data(geographic_data_path)
    _plot_geographic_points(geographic_data, global_shapefile_data_path, path_rose_wind)
    plt.savefig(result_map_path)


@cli.command()
def plot_geographic_points_by_trip(
    geographic_data_path: str = typer.Option(),
    global_shapefile_data_path: str = typer.Option(),
    path_rose_wind: str = typer.Option(),
    result_map_path: str = typer.Option(),
):
    geographic_data = adapt_geographic_data(geographic_data_path)
    _plot_geographic_points_by_trip(geographic_data, global_shapefile_data_path, path_rose_wind)
    plt.savefig(result_map_path)


@cli.command()
def plot_geographic_points_by_vessel(
    geographic_data_path: str = typer.Option(),
    global_shapefile_data_path: str = typer.Option(),
    path_rose_wind: str = typer.Option(),
    result_map_path: str = typer.Option(),
):
    geographic_data = adapt_geographic_data(geographic_data_path)
    _plot_geographic_points_by_vessel(geographic_data, global_shapefile_data_path, path_rose_wind)
    plt.savefig(result_map_path)


@cli.command()
def boxplot(
    data_path: str = typer.Option(),
    columns_of_interest: str = typer.Option(),
    boxplot_path: str = typer.Option(),
):
    summary_data = pd.read_csv(data_path)
    columns = columns_of_interest.split(",")
    print(columns)
    data_for_boxplot = create_box_plot_data_from_columns(summary_data, columns)
    create_box_plot(data_for_boxplot)
    plt.savefig(boxplot_path)


@cli.command()
def version():
    print(gp.__version__)
