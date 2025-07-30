"""UMAP visualization for dataset."""

from typing import Literal

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from umap.umap_ import UMAP

from explore.containers.correlations import constants
from explore.containers.correlations.st_explanations import st_UMAP_explanation


@st.cache_data
def plot_umap(
    df: pd.DataFrame,
    color_feature: str = None,
    n_components: int = 3,
    efficiency_vs_reproducibility: Literal[
        "Reproducibility of results", "Parallelization of process"
    ] = "Reproducibility of results",
) -> None:
    """Plot UMAP visualization for the dataset, coloring points by a specified feature.

    Args:
        df (pd.DataFrame): The input DataFrame containing the data.
        color_feature (str): The name of the categorical feature to color points by.
        n_components (int): The number of dimensions for UMAP. Default is 3 for 3D visualization.
        efficiency_vs_reproducibility (str): The mode to use for UMAP. Valid values are "Reproducibility of results" and "Parallelization of process". This will determine the number of jobs used for the computation and/or the seed to use for reproducibility.

    Returns:
        None
    """
    # Select numeric data and filter columns with less than 80% missing values
    df_numeric = df.select_dtypes(include=[np.number])
    df_numeric = df_numeric.loc[:, (df_numeric.isnull().mean() < 0.8)]
    df_numeric.dropna(inplace=True)

    # TODO: Handle non-numerical values to include them in the UMAP visualization (e.g. one-hot encoding, use another distance metric, etc.)

    # Initialize UMAP with specified number of components
    if efficiency_vs_reproducibility == "Parallelization of process":
        reducer = UMAP(n_components=n_components, n_jobs=-1)
    else:
        reducer = UMAP(n_components=n_components, random_state=constants.RANDOM_STATE, n_jobs=1)

    embedding = reducer.fit_transform(df_numeric)

    # Determine whether to color the points based on the color_feature
    color_argument = {}
    if color_feature:
        df_color = df.loc[df_numeric.index, color_feature]
        color_argument["color"] = df_color.values

    # Plot
    if n_components == 3:
        # 3D Plot
        fig = px.scatter_3d(
            x=embedding[:, 0],
            y=embedding[:, 1],
            z=embedding[:, 2],
            title="UMAP 3D projection of the dataset",
            **color_argument,  # Apply color argument if present
        )
    else:
        # 2D Plot
        fig = px.scatter(
            x=embedding[:, 0],
            y=embedding[:, 1],
            title="UMAP 2D projection of the dataset",
            **color_argument,  # Apply color argument if present
        )

    fig.update_layout()
    fig.update_traces(marker=dict(size=4))
    st.write(f"UMAP ({n_components}D) Visualization colored by '{color_feature}'")
    st.plotly_chart(fig)
    st_UMAP_explanation()
