"""Metrics container."""

import dvc.api
import pandas as pd
import streamlit as st


def metrics_container() -> None:
    metrics = dvc.api.metrics_show()
    st.subheader("Metrics")
    try:
        st.write(pd.DataFrame(metrics).T)
    except:
        st.warning(
            "Format your metrics with the following format: "
            + "{'model1': {'metric1': value1, 'metric2': value2}, 'model2': {'metric1': value1, 'metric2': value2}}"
        )
