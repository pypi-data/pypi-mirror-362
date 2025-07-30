"""Streamlit app for data exploration."""

import pathlib

import streamlit as st

from explore.constants import NROWS
from explore.containers.cockpit_container.main import cockpit_container
from explore.containers.columns_stats_container.main import columns_stats_container
from explore.containers.correlations.main import correlation_container
from explore.containers.data_exploration.main import explorer_container
from explore.containers.experiments.main import experiments_container
from explore.containers.metrics.main import metrics_container
from explore.containers.model.main import model_container
from explore.containers.params.main import params_container
from explore.containers.sample_df.main import display_sample_df_container
from explore.io import read_df_top_rows
from explore.sidebar import MenuTitles, set_side_bar
from explore.utils import parse_dvc_steps_from_dvc_yaml

DATA_PATH = pathlib.Path("data")


st.set_page_config(layout="wide")


def main() -> None:
    """Main function for the Streamlit app."""
    cockpit_col, metrics_params_col = st.columns([1, 1])
    dvc_steps = parse_dvc_steps_from_dvc_yaml()

    view_name = set_side_bar()

    with cockpit_col:
        file_path, dvc_step_key = cockpit_container(dvc_steps=dvc_steps)

    with metrics_params_col:
        with st.container(border=True):
            params_container()
            metrics_container()

    if file_path:
        sample_df = read_df_top_rows(file_path, nrows=NROWS)
        columns = list(sample_df.columns)

        display_sample_df_container(sample_df)
        if view_name == MenuTitles.EDA:
            explorer_container(file_path, dvc_step_key, columns=columns)
        elif view_name == MenuTitles.COLUMNS_STATS:
            columns_stats_container(file_path)
        elif view_name == MenuTitles.CORRELATION:
            schema_dict = sample_df.dtypes.to_dict()
            correlation_container(file_path, dvc_step_key, schema_dict=schema_dict)
        elif view_name == MenuTitles.EXPERIMENTS:
            experiments_container()
        elif view_name == MenuTitles.MODEL:
            model_container()

    else:
        st.warning("No parquet file found for this DVC step.")


if __name__ == "__main__":
    main()
