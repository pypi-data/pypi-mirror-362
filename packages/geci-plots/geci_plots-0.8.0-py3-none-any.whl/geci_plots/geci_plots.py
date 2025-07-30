#!/usr/bin/env python

from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

import matplotlib
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def setup_matplotlib(font_family, dpi):
    matplotlib.rcParams["figure.dpi"] = dpi
    matplotlib.rcParams["font.family"] = font_family
    matplotlib.rcParams["mathtext.fontset"] = "stix"
    matplotlib.use("Agg")


cmap = plt.get_cmap("tab10")
zones_colors = cmap(np.arange(9))

islet_markers = {
    "Asuncion": "o",
    "Coronado": "^",
    "Morro Prieto and Zapato": "s",
    "Guadalupe": "X",
    "Natividad": "p",
    "San Benito": "h",
    "San Jeronimo": "D",
    "San Martin": "P",
    "San Roque": "*",
    "Todos Santos": ">",
}

islet_colors = {
    "Asuncion": "black",
    "Coronado": "red",
    "Morro Prieto and Zapato": "peru",
    "Guadalupe": "gold",
    "Natividad": "green",
    "San Benito": "blue",
    "San Jeronimo": "purple",
    "San Martin": "hotpink",
    "San Roque": "lightgreen",
    "Todos Santos": "skyblue",
}


def geci_plot(font_family="STIXGeneral", dpi=300, figsize=(11, 8)):
    setup_matplotlib(font_family, dpi)
    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    plt.yticks(rotation=90)
    return fig, ax


def plot_histogram_with_limits(x, bins, limits=[], plot_options={}, lines_options={}):
    _, ax = geci_plot()
    ax.hist(x, bins=bins, **plot_options)
    for lines in limits:
        ax.axvline(x=lines, **lines_options)
    return ax


def rounddown(x, multiplier):
    return np.floor(x / multiplier) * multiplier


def roundup(x, multiplier):
    return np.ceil(x / multiplier) * multiplier


def fix_date(date):
    return (
        date.replace("Abr", "Apr").replace("Ene", "Jan").replace("Ago", "Aug").replace("Dic", "Dec")
    )


def set_map_tick_labels(fontsize=15):
    ejes = plt.gca()
    y_min, y_max = ejes.get_ylim()
    plt.yticks(
        [
            int(limite)
            for i_limite, limite in enumerate(np.linspace(y_min, y_max, 5))
            if i_limite > 0
        ],
        [
            f"{limite:.0f} mN" if i_limite == 4 else int(limite)
            for i_limite, limite in enumerate(np.linspace(y_min, y_max, 5))
            if i_limite > 0
        ],
        fontsize=fontsize,
    )

    ejes = plt.gca()
    x_min, x_max = ejes.get_xlim()
    plt.xticks(
        [
            int(limite)
            for i_limite, limite in enumerate(np.linspace(x_min, x_max, 5))
            if i_limite > 0
        ],
        [
            f"{limite:.0f} mE" if i_limite == 4 else int(limite)
            for i_limite, limite in enumerate(np.linspace(x_min, x_max, 5))
            if i_limite > 0
        ],
        fontsize=fontsize,
    )


def set_scale_bar(ax, length, width, loc="lower right", fontsize=10):
    fontprops = fm.FontProperties(size=fontsize)
    scalebar = AnchoredSizeBar(
        ax.transData,
        length,
        f"{length} m",
        loc,
        pad=0.1,
        color="black",
        frameon=False,
        size_vertical=width,
        fontproperties=fontprops,
    )
    ax.add_artist(scalebar)


def plot_location_plot(ax, linea_costa, margen_x, margen_y, box_length=500):
    axins = ax.inset_axes([0.05, 0.50, 0.2, 0.45])
    axins.fill(
        linea_costa.x, linea_costa.y, facecolor="#fffae6", edgecolor="black", linewidth=1, zorder=0
    )

    margen_subplot_x = np.array(margen_x) + np.array([-box_length, box_length])
    margen_subplot_y = np.array(margen_y) + np.array([-box_length, box_length])

    axins.set_xticklabels("")
    axins.set_yticklabels("")
    axins.set_facecolor("#E6FFFF")
    axins.set_xticks([])
    axins.set_yticks([])
    axins.plot(
        [
            margen_subplot_x[1],
            margen_subplot_x[0],
            margen_subplot_x[0],
            margen_subplot_x[1],
            margen_subplot_x[1],
        ],
        [
            margen_subplot_y[0],
            margen_subplot_y[0],
            margen_subplot_y[1],
            margen_subplot_y[1],
            margen_subplot_y[0],
        ],
        "red",
        linewidth=2,
    )

    for axis in ["top", "bottom", "left", "right"]:
        axins.spines[axis].set_linewidth(2)


def rounded_ticks_array(superior_limit, min_value):
    ticks_array = np.arange(
        np.floor(min_value - min_value * 0.15),
        roundup(superior_limit * 1.2, 10 ** order_magnitude(superior_limit)),
        roundup(superior_limit * 0.2, 10 ** order_magnitude(superior_limit)),
    )
    return ticks_array


def ticks_positions_array(x):
    ticks_positions = np.linspace(1, len(x), len(x))
    ticks_positions[-1] = ticks_positions[-1] + 0.05
    return ticks_positions


def sort_monthly_dataframe(df, date_format="GECI", column_key="Date"):
    if date_format == "GECI":
        df[column_key] = df.Date.apply(lambda fecha: fix_date(str(fecha)))
        df[column_key] = pd.to_datetime(df[column_key], format="%Y/%b")
    elif date_format == "ISO-8601":
        df[column_key] = pd.to_datetime(df[column_key], format="%Y-%m")
    df = df.sort_values(by=[column_key]).reset_index(drop=True)
    return df.set_index([column_key])


def order_magnitude(x):
    return int(np.floor(np.log10(np.max(x))))


def generate_monthly_ticks(df, bar_gap=2):
    ticks_labels = df.index.strftime("%b - %Y")
    ticks_positions = np.linspace(1, len(df), len(df)) * bar_gap
    return [ticks_positions, ticks_labels]


def generate_weekly_ticks(df, bar_gap=2):
    ticks_labels = df.index.strftime("%d - %b")
    ticks_positions = np.linspace(1, len(df), len(df)) * bar_gap
    return [ticks_positions, ticks_labels]


def select_date_interval(df, initial_date, final_date=pd.Timestamp.today()):
    return df.loc[initial_date:final_date]


def annotated_bar_plot(
    ax,
    df,
    x_ticks,
    fontsize=15,
    bar_label_size=15,
    bar_gap=2,
    x_pos=-0.5,
    y_pos=200,
    column_key="Effort",
):
    data_length = len(df)
    ax.bar(x_ticks[0], df[column_key], alpha=1, width=0.9, zorder=0)
    plt.xticks(x_ticks[0], x_ticks[1], rotation=90, size=fontsize)
    ax.set_ylim(0, roundup(df[column_key].max(), 10 ** order_magnitude(df[column_key])))
    annotate_bars_with_values(df[column_key], x_ticks, x_pos, y_pos, bar_label_size)
    ax.tick_params(labelsize=fontsize)
    plt.xlim(0.5, data_length * bar_gap + 1)


def add_text(i, data_array, x_ticks, x_pos=-0.5, y_pos=200, fontsize=15):
    plt.text(
        x=x_ticks[0][i] + x_pos,
        y=data_array.iloc[i] + y_pos,
        s=data_array.iloc[i],
        size=fontsize,
    )


def annotate_plot_with_values(data_array, x_ticks, x_pos=-0.5, y_pos=200, fontsize=15):
    for i in range(len(data_array)):
        if data_array.iloc[i] < np.mean(data_array):
            add_text(i, data_array, x_ticks, x_pos, -y_pos * 1.3, fontsize)
        else:
            add_text(i, data_array, x_ticks, x_pos, y_pos, fontsize)


def annotate_bars_with_values(data_array, x_ticks, x_pos=-0.5, y_pos=200, fontsize=15):
    for i in range(len(data_array)):
        if data_array.iloc[i] != 0:
            add_text(i, data_array, x_ticks, x_pos, y_pos, fontsize)


def plot_points_with_labels(
    ax, df, x_ticks, fontsize=15, label_fontsize=15, x_pos=-0.4, y_pos=5, column_key="Effort"
):
    ax.plot(x_ticks[0], df[column_key], c="black", marker="D", label=column_key)
    annotate_plot_with_values(df[column_key], x_ticks, x_pos, y_pos, label_fontsize)
    ax.set_ylim(0, roundup(df[column_key].max() * 1.5, 10 ** order_magnitude(df[column_key])))
    ax.spines["top"].set_visible(False)
    ax.tick_params(labelsize=fontsize)


def annotated_bar_plot_by_columns(
    ax,
    df,
    x_ticks,
    colors_array=zones_colors,
    fontsize=15,
    bar_label_size=15,
    bar_gap=2,
    x_pos=-0.5,
    y_pos=200,
):
    data_length = len(df)
    bottom = data_length * [0]
    columns_keys = df.keys().values
    for i in range(len(columns_keys)):
        plt.bar(
            x_ticks[0],
            df[columns_keys[i]],
            bottom=bottom,
            label="{}".format(columns_keys[i].replace("_", " ")),
            color=colors_array[i],
        )
        bottom = bottom + df[columns_keys[i]]
    xticks_lim = x_ticks[0][-1] + 1
    plt.xticks([*x_ticks[0], xticks_lim], [*x_ticks[1], ""], rotation=90, size=fontsize)
    annotate_bars_with_values(bottom, x_ticks, x_pos, y_pos, fontsize=bar_label_size)
    ax.set_ylim(0, roundup(bottom.max() * 1.3, 10 ** order_magnitude(bottom)))
    ax.tick_params(labelsize=fontsize)
    plt.legend(ncol=4, frameon=False, fontsize=fontsize, loc="upper center")
    plt.xlim(0.5, data_length * bar_gap + 1)


def plot_comparative_annual_effort_by_zone(
    ax, df, fontsize=15, bar_label_size=15, bar_gap=3, column_key="Effort"
):
    seasons = df.Season.unique()
    x_ticks_labels = df.Zone.unique()
    n_bars = len(x_ticks_labels)
    x_ticks = [df.Zone.unique() * bar_gap, df.Zone.unique()]
    gap_seasons = 0
    for i in seasons:
        seasonal_data = df[column_key][df["Season"] == i]
        plt.bar(x_ticks[0] + gap_seasons, seasonal_data, label=f"{i}")
        annotate_bars_with_values(
            seasonal_data, x_ticks, x_pos=-0.55 + gap_seasons, y_pos=200, fontsize=bar_label_size
        )
        gap_seasons += 1
    ax.set_ylabel("Annual effort per zone (night traps)", fontsize=fontsize)
    ax.set_xlabel("Zones", fontsize=fontsize)
    ax.set_ylim(0, roundup(df[column_key].max(), 10 ** order_magnitude(df[column_key])))
    ax.tick_params(labelsize=fontsize)
    plt.legend(ncol=4, frameon=False, fontsize=fontsize)
    xticks_lim = n_bars * bar_gap + 2
    plt.xticks([*x_ticks[0], xticks_lim], [*x_ticks[1], ""], size=fontsize)
    plt.xlim(1, n_bars * bar_gap + 2)


def calculate_anotations_positions_for_wedges(wedges):
    x = np.array([np.cos(np.deg2rad(central_wedge_angle(wedge))) for i, wedge in enumerate(wedges)])
    y = np.array([np.sin(np.deg2rad(central_wedge_angle(wedge))) for i, wedge in enumerate(wedges)])
    return x, y


def calculate_anotations_positions_for_wedges_2(angle):
    x = np.cos(np.deg2rad(angle))
    y = np.sin(np.deg2rad(angle))
    return x, y


def scale_anotations_y_positions(y_positions, scale_y):
    return np.linspace(
        np.min(y_positions) - scale_y, np.max(y_positions) + scale_y, len(y_positions)
    )


def central_wedge_angle(wedge):
    return (wedge.theta2 - wedge.theta1) / 2.0 + wedge.theta1


def annotate_pie_chart(ax, wedges, box_labels, scale_x=1.35, scale_y=1.4, fontsize=15):
    bbox_props = dict(boxstyle="round,pad=0.3,rounding_size=0.5", fc="w", ec="k", lw=0.72)
    kw = dict(
        arrowprops=dict(arrowstyle="-"),
        bbox=bbox_props,
        zorder=0,
        ha="center",
        va="center",
        size=fontsize,
    )
    x, y = calculate_anotations_positions_for_wedges(wedges)
    x_negative_mask = x <= 0
    x_positive_mask = x >= 0
    y_text_left = scale_anotations_y_positions(y[x_negative_mask], scale_y)
    y_text_right = scale_anotations_y_positions(y[x_positive_mask], scale_y)
    y_text = y.copy()
    y_text[x_negative_mask] = y_text_left
    y_text[x_positive_mask] = y_text_right
    y_returned = []
    for i, wedge in enumerate(wedges):
        central_angle = central_wedge_angle(wedge)
        x, y = calculate_anotations_positions_for_wedges_2(central_angle)
        x_sign = np.sign(x)
        horizontalalignment = {-1: "right", 1: "left"}[int(x_sign)]
        vertical_scaling = {True: -1, False: +1}[y <= 0]
        connectionstyle = "arc3,rad=0.1"
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        ax.annotate(
            box_labels[i],
            xy=(x, y),
            xytext=(scale_x * x_sign, scale_y * vertical_scaling + y),
            horizontalalignment=horizontalalignment,
            **kw,
        )
        y_returned.append(y)
    return y_text, y_returned


def filter_by_season_and_zone(df, season, zone):
    return df[(df.Season == season) & (df.Zone == zone)]


def generate_pie_labels_for_sex(n, f_percent, m_percent, ni_percent):
    return "Zone {:.0f}\n F:{:.2f}% M:{:.2f}% NI:{:.2f}%".format(
        n, f_percent, m_percent, ni_percent
    )


def generate_pie_labels_for_age(n, j_percent, a_percent, ni_percent):
    return "Zone {:.0f}\n J:{:.2f}% A:{:.2f}% NI:{:.2f}%".format(
        n, j_percent, a_percent, ni_percent
    )


def calculate_values_for_sex_pie_chart(df, season):
    seasons = []
    labels = []
    zones = df.Zone.unique().astype(int)
    for i in zones:
        data_filtered = filter_by_season_and_zone(df, season, i)
        seasons.append(
            [
                data_filtered["Female_captures"].values[0],
                data_filtered["Male_captures"].values[0],
                data_filtered["Not_available"].values[0],
            ]
        )
        labels.append(
            generate_pie_labels_for_sex(
                i,
                data_filtered["First_class_percent"].values[0],
                data_filtered["Second_class_percent"].values[0],
                data_filtered["NA_percent"].values[0],
            )
        )
    return np.array(seasons), np.array(labels)


def calculate_percent(df, column_key="Male_captures", new_column_key="Male_percent"):
    df[new_column_key] = df[column_key] / df.Total_captures * 100


def prepare_cats_by_zone_and_sex(df):
    calculate_percent(df, column_key="Male_captures", new_column_key="Second_class_percent")
    calculate_percent(df, column_key="Female_captures", new_column_key="First_class_percent")
    calculate_percent(df, column_key="Not_available", new_column_key="NA_percent")
    return df


def prepare_cats_by_zone_and_age(df):
    calculate_percent(df, column_key="Juvenile_captures", new_column_key="First_class_percent")
    calculate_percent(df, column_key="Adult_captures", new_column_key="Second_class_percent")
    calculate_percent(df, column_key="Not_available", new_column_key="NA_percent")
    return df


def calculate_values_for_age_pie_chart(df, season):
    seasons = []
    labels = []
    zones = df.Zone.unique().astype(int)
    for i in zones:
        data_filtered = filter_by_season_and_zone(df, season, i)
        seasons.append(
            [
                data_filtered["Juvenile_captures"].values[0],
                data_filtered["Adult_captures"].values[0],
                data_filtered["Not_available"].values[0],
            ]
        )
        labels.append(
            generate_pie_labels_for_age(
                i,
                data_filtered["First_class_percent"].values[0],
                data_filtered["Second_class_percent"].values[0],
                data_filtered["NA_percent"].values[0],
            )
        )
    return np.array(seasons), np.array(labels)


def historic_mean_effort(df, column_key):
    return df[column_key].mean()


def plot_mean_effort_line(ax, mean_effort):
    ax.plot([-100, 1000], [mean_effort, mean_effort], "-r", label="Mean effort")


def set_axis_labels(ax, variable):
    ax.set_xlabel("Temporadas", fontsize=25, labelpad=10)
    if variable == "Masa_del_individuo":
        ax.set_ylabel(f'{variable.replace("_", " ")} (gr)', fontsize=25, labelpad=10)
    else:
        ax.set_ylabel(f'{variable.replace("_", " ")} (cm)', fontsize=25, labelpad=10)


def set_box_plot_style(ax, df, seasons):
    ticks_positions = ticks_positions_array(seasons)
    upper_limit = roundup(np.max(df), 10)
    plt.ylim(0, upper_limit)
    rounded_ticks = rounded_ticks_array(upper_limit, 0)
    plt.yticks(rounded_ticks, size=20)
    ax.tick_params(axis="y", labelsize=20, labelrotation=90)
    ax.tick_params(axis="x", labelsize=20)
    plt.xticks(ticks_positions, seasons, size=20, color="k")


def heatmap(
    data, row_labels, col_labels, labels_size=15, ax=None, cbar_kw={}, cbarlabel="", **kwargs
):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    im = ax.imshow(data, **kwargs)

    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=90, va="bottom", labelpad=30, size=15)

    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    ax.set_xticklabels(col_labels, size=labels_size)
    ax.set_yticklabels(row_labels, size=labels_size)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")

    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xticks(np.arange(data.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="w", linestyle="-", linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(
    im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"), threshold=None, **textkw
):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max()) / 2.0
    kw = dict(horizontalalignment="center", verticalalignment="center")
    kw.update(textkw)
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return text
