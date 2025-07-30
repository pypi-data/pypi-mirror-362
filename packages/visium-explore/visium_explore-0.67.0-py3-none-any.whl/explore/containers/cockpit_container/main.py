"""Definition of the cockpit container."""

import json
import pathlib
import subprocess

import pandas as pd
import streamlit as st

from explore.containers.cockpit_container.data_artifact_selection import data_artifact_selection_container
from explore.containers.cockpit_container.graph_container import graph_container
from explore.utils import DVCStep


def cockpit_container(dvc_steps: list[DVCStep]) -> tuple[pathlib.Path, str]:
    cockpit_container = st.container(border=True)
    with cockpit_container:
        st.header("Cockpit")
        col1, col2 = st.columns([1, 1])
        with col1:
            file_path, dvc_step_key = data_artifact_selection_container(dvc_steps)
            st.write("---")

            status, color = parse_dvc_status()
            st.write(f"Pipeline up to date: {color}")

            if len(status) > 0:
                status_df = pd.DataFrame(status)
                st.write(status_df.T)

            st.write("**Commands**:")
            st.button("Reproduce Pipeline", key="reproduce_button", on_click=dvc_repro_command)
            st.download_button(label="Download Selected Data (Coming)", data="todo", file_name=None, disabled=True)
        with col2:
            graph_container()

    return file_path, dvc_step_key


def dvc_repro_command() -> None:
    """Execute a dvc repro bash command."""
    # Execute a dvc repro bash command
    subprocess.run(["dvc", "repro"], check=True, capture_output=True)


def parse_dvc_status() -> dict:
    dvc_status_output = subprocess.run(["dvc", "status", "--json"], capture_output=True, text=True, check=True).stdout
    status_dict = json.loads(dvc_status_output)
    color = ":large_green_circle:" if len(status_dict) == 0 else ":red_circle:"
    return status_dict, color
