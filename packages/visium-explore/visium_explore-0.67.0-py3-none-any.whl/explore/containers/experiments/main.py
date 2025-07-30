"""Experiment tracking container."""

import dvc.api
import pandas as pd
import streamlit as st


def experiments_container() -> None:
    st.header("Experiments tracking")
    exps = dvc.api.exp_show()
    df_exps = pd.DataFrame(exps)
    st.write(df_exps)
    return None
