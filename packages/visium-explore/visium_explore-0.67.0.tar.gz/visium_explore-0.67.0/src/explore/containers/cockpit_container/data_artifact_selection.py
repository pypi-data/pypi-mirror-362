"""Streamlit container for selecting a data artifact in a DVC step."""

import pathlib

import streamlit as st

from explore.utils import DVCStep


def data_artifact_selection_container(dvc_steps: list[DVCStep]) -> tuple[pathlib.Path, str]:
    selected_dvc_step = st.selectbox(label="DVC Step selection", options=dvc_steps, format_func=lambda x: x.name)
    dvc_step_key = f"select_box_{selected_dvc_step.name}"
    parquet_files_path_list = discover_parquet_files(selected_dvc_step.output_path)
    if len(parquet_files_path_list) > 0:
        file_path = select_file_container(parquet_files_path_list, dvc_step_key)
    else:
        st.warning("No output parquet data found for this DVC step.")
        file_path = None
    return file_path, dvc_step_key


def select_file_container(parquet_data_path_list: pathlib.Path, tab_key: str) -> pathlib.Path:
    """Container for selecting a file in the DVC step."""

    def _format_path(path: pathlib.Path) -> str:
        return path.parts[-1]

    file_path = st.selectbox(
        "Select a file in the DVC step:",
        options=parquet_data_path_list,
        format_func=_format_path,
        key=tab_key,
    )
    return file_path


def discover_parquet_files(dvc_step_data_path: pathlib.Path) -> list[pathlib.Path]:
    """Returns a list of parquet files found in the input path."""
    if dvc_step_data_path is None:
        return []
    list_of_files = list(dvc_step_data_path.glob("*"))
    return [path for path in list_of_files if path.suffix == ".parquet"]
