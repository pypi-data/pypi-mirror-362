"""The explorer container allows the user to interact with the chosen data by selecting columns to explore and plot."""

import pathlib

import pandas as pd
import streamlit as st

from explore.containers.data_exploration.constants import PlotTypes
from explore.containers.data_exploration.plot import Box, Histogram, Line, Plot, Scatter
from explore.io import read_df
from explore.utils import build_and_display_column_stats, build_column_stats, display_column_stats


def explorer_container(file_path: pathlib.Path, tab_key: str, columns: list[str]) -> None:
    """Display the explorer container.

    It allows the user to interact with the chosen data by selecting columns to explore and plot.
    """
    st.write("---")
    st.header("Data exploration")

    file_path = pathlib.Path(file_path)
    dvc_step = file_path.parts[-1]

    col1, col2 = st.columns([1, 2])
    with col1:
        with st.container(border=True):
            st.subheader("User inputs")
            plot, x_axis, y_axis = column_of_interest_and_plot_selection_container(
                tab_key=tab_key, dvc_step=dvc_step, columns=columns
            )

    with col2:
        with st.container(border=True):
            st.subheader("Results")
            display_plot_container(file_path=file_path, plot=plot, x_axis=x_axis, y_axis=y_axis)

        # exploration_container(file_path, user_inputs=user_inputs)


def column_of_interest_and_plot_selection_container(
    tab_key: str, dvc_step: str, columns: list
) -> tuple[Plot, str, str]:
    key = f"{tab_key}_{dvc_step}"
    x_axis = st.selectbox(
        "Select the **x-axis**",
        options=sorted(columns),
        key=f"x_axis_select_{key}",
    )
    y_axis = st.selectbox(
        "Select the **y-axis**",
        options=sorted(columns),
        index=None,
        key=f"y_axis_select_{key}",
    )
    plot_type = st.selectbox(
        "Select the type of plot you want to use",
        options=[None, PlotTypes.HISTOGRAM, PlotTypes.BOX, PlotTypes.SCATTER, PlotTypes.LINE],
        key=f"plot_type_{key}",
    )

    if plot_type == PlotTypes.HISTOGRAM:
        plot = Histogram(columns=columns, key=key)
    elif plot_type == PlotTypes.BOX:
        plot = Box(columns=columns, key=key)
    elif plot_type == PlotTypes.SCATTER:
        plot = Scatter(columns=columns, key=key)
    elif plot_type == PlotTypes.LINE:
        plot = Line(columns=columns, key=key)
    else:
        plot = None
        st.warning("Please select a plot type above to choose plot options.")

    return plot, x_axis, y_axis


def display_plot_container(file_path: pathlib.Path, plot: Plot, x_axis: str, y_axis: str) -> None:
    """Read the data and display the plot with the settings specified by the Plot object."""
    df = read_df(file_path)

    st.write("##### Univariate description")
    # x axis description

    col1, col2 = st.columns([1, 1])

    with col1:
        st.write(f"**{x_axis} (x - axis)**")
        # univariate_description_df = construct_univariate_description_df(df, x_axis)
        # st.write(univariate_description_df)
        build_and_display_column_stats(df[[x_axis]])

        if y_axis is not None:
            st.write(f"**{y_axis} (y - axis)**")
            build_and_display_column_stats(df[[y_axis]])
            # univariate_description_df = construct_univariate_description_df(df, y_axis)
            # st.write(univariate_description_df)

    with col2:
        if x_axis and y_axis and pd.api.types.is_object_dtype(df[y_axis]):
            # grpby_y_axis = df.groupby(y_axis)
            # display_column_stats(grpby_y_axis[[x_axis]])

            display_stats_by_group(df=df, var=x_axis, group=y_axis)

        if y_axis and x_axis and pd.api.types.is_object_dtype(df[x_axis]):
            display_stats_by_group(df=df, var=y_axis, group=x_axis)

    st.write("---")
    st.write("##### Plot")
    if plot is not None:
        plot.show(df=df, x_axis=x_axis, y_axis=y_axis)
    else:
        st.warning("Please select a plot type on the left.")


def construct_univariate_description_df(df: pd.DataFrame, selected_col: str) -> pd.DataFrame:
    """Compute the univariate description of the selected column."""
    univariate_description_series = df[selected_col].describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])

    univariate_description_df = pd.DataFrame(univariate_description_series).transpose()
    univariate_description_df = univariate_description_df.drop(columns=["count"])
    describe_columns = list(univariate_description_df.columns)
    univariate_description_df["ratio_null"] = df[selected_col].isnull().mean()
    univariate_description_df["size"] = len(df)
    univariate_description_df = univariate_description_df[["size", "ratio_null"] + describe_columns]
    return univariate_description_df


def display_stats_by_group(df: pd.DataFrame, var: str, group: str) -> None:
    assert var is not None
    assert pd.api.types.is_object_dtype(df[group]), "group must be a categorical column."
    st.write(f"**{var}** grouped by **{group}**")
    groups = df.groupby(group)

    stats_df_list = []
    name_list = []
    for name, group_df in groups:
        group_stats_df = build_column_stats(group_df[[var]])
        stats_df_list.append(group_stats_df)
        name_list.append(name)

    stats_df = pd.concat(stats_df_list, axis=0)
    stats_df.index = name_list
    stats_df.index.name = group
    display_column_stats(stats_df)
