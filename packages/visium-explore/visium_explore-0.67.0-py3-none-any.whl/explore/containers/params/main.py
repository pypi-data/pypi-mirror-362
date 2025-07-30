"""Params container."""

import dvc.api
import pandas as pd
import streamlit as st


def params_container() -> None:
    st.subheader("Params")
    params = dvc.api.params_show()
    df_params = pd.DataFrame([params], index=["params"])
    st.write(df_params)
