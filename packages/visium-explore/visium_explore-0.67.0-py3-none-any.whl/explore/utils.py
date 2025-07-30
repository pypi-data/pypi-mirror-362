"""Utility functions for the explore module."""

import pathlib
from typing import Optional

import pandas as pd
import pandera as pa
import streamlit as st
import yaml
from pydantic import BaseModel  # pylint: disable=no-name-in-module

from explore.constants import DVC_OUTS_KEY


def get_path_last_part(list_of_full_path: list[pathlib.Path]) -> list[str]:
    """Returns a list with the last part of the path for each path in the list."""
    list_of_last_part = [path.parts[-1] for path in list_of_full_path]
    return list_of_last_part


class DVCStep(BaseModel):
    """Data model representing a DVC step."""

    name: str
    output_path: Optional[pathlib.Path]


def parse_dvc_steps_from_dvc_yaml() -> list[DVCStep]:
    """Parse the DVC steps from the dvc.yaml file."""
    with open("dvc.yaml", "r", encoding="utf-8") as f:
        dvc_yaml = yaml.safe_load(f)

    stages_dict = dvc_yaml["stages"]
    steps = []
    for stage_name, stage_content in stages_dict.items():
        if DVC_OUTS_KEY in stage_content:
            output_path = stage_content[DVC_OUTS_KEY][0]
        else:
            output_path = None

        steps.append(DVCStep(name=stage_name, output_path=output_path))
    return steps


def build_and_display_column_stats(df: pd.DataFrame) -> None:
    """Build and display the stats for the columns of the DataFrame."""
    stats_df = build_column_stats(df)
    display_column_stats(stats_df)


def display_column_stats(stats_df: pd.DataFrame) -> None:
    """Take the output of build_column_stats and display it in a Streamlit dataframe."""
    st.dataframe(
        stats_df,
        column_config={ColumnStats.RATIO_NULL: st.column_config.ProgressColumn("Ratio null", min_value=0, max_value=1)},
    )


def build_column_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Build the stats for the columns of the DataFrame."""
    stats_df = df.describe().transpose()
    stats_df = stats_df.drop(["count"], axis=1)
    stats_df[ColumnStats.RATIO_NULL] = df.isnull().mean()
    stats_df[ColumnStats.TYPE] = df.dtypes

    # Reorder columns
    columns_list = stats_df.columns.tolist()
    columns_list.remove(ColumnStats.TYPE)
    columns_list.remove(ColumnStats.RATIO_NULL)
    columns_list = [ColumnStats.TYPE, ColumnStats.RATIO_NULL] + columns_list

    stats_df = stats_df[columns_list]
    return stats_df


class ColumnStats(pa.DataFrameModel):
    """Pandera model for the column stats."""

    TYPE = "type"
    RATIO_NULL = "ratio_null"
