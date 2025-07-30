from geci_plots.geci_plots import geci_plot


def create_box_plot(boxplotdata):
    labels = [serie.name for serie in boxplotdata]
    fig, ax = geci_plot()
    ax.boxplot(boxplotdata, tick_labels=labels)
    return fig, ax


def create_box_plot_data(data_feature, column_name):
    """This functions takes a DataFrame and reurns array for boxplot

    Args:
        data_feature (DataFrame): DataFrame with colum "Temporada" and column_name
        column_name (string): Name of the column you want to plot

    Returns:
        array: array prepared for input in plt.boxplot
        array: unique seasons
    """
    boxsplotdata = []
    seasons = data_feature["Temporada"].unique()
    for i in seasons:
        masked_data_feature = data_feature[data_feature["Temporada"] == i]
        boxsplotdata.append(*create_box_plot_data_from_columns(masked_data_feature, [column_name]))
    return boxsplotdata, seasons


def create_box_plot_data_from_columns(df, columns):
    box_plot_data = []
    for column in columns:
        data_feature = df[column]
        box_plot_data.append(data_feature)
    return box_plot_data
