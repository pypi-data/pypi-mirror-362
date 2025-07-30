"""Container allowing to interact with the model."""

import mlflow.pyfunc
import streamlit as st

from explore.containers.model.constants import MLFLOW_PATH


def model_container() -> None:
    st.header("Model exploration")
    try:
        model = mlflow.pyfunc.load_model(MLFLOW_PATH)
        signature = model._model_meta._signature
        col1, col2 = st.columns([1, 4])
        with col1:
            with st.form("model_inputs"):
                st.subheader("Model Inputs")
                for i in signature.inputs.to_dict():
                    if i["type"] == "double":
                        st.number_input(i["name"])
                st.form_submit_button("Submit")
        with col2:
            with st.container(border=True):
                st.subheader("Model Outputs")
                st.warning("Work in progress... Coming soon!")
            # st.write(i)
            # st.write(type(i))

    except OSError:
        st.warning(
            "No MLFlow model found for this DVC step."
            + f"Please save your model with the MLFlow format at {MLFLOW_PATH}"
        )
