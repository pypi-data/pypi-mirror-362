"""Sidebar for the explore module."""

import os

import streamlit as st


class MenuTitles:
    """Class containing the titles for the sidebar menu."""

    EDA = "Univariate and bivariate EDA"
    CORRELATION = "Correlation study"
    EXPERIMENTS = "Experiments tracking"
    MODEL = "Model deployment"
    COLUMNS_STATS = "Columns statistics"


def set_side_bar() -> str:
    """Set the sidebar with the logo and title."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = "resources/horizontal-color.svg"
    absolute_path = os.path.join(current_dir, relative_path)

    st.sidebar.image(absolute_path, width=175)
    st.sidebar.title("Explore")

    with st.sidebar:
        view_name = st.radio(
            "Sidebar radio buttons",
            options=[
                MenuTitles.COLUMNS_STATS,
                MenuTitles.EDA,
                MenuTitles.CORRELATION,
                MenuTitles.EXPERIMENTS,
                MenuTitles.MODEL,
            ],
            # key="theme",
        )
    return view_name
