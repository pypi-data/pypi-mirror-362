"""Module for the different plot types, their settings and their corresponding streamlit selectors."""

import abc

import pandas as pd
import plotly.express as px
import streamlit as st


class Plot:
    """Base class for the different plot types, their settings and their corresponding streamlit selectors."""

    def __init__(self, columns: list, key: str):
        """Construct Plot object."""
        st.markdown("---")

        self.form = st.form(key=f"form_{key}", border=False)
        with self.form:
            self.show_form(columns=columns, key=key)
        self.form.form_submit_button(label="Submit")

    def show_form(self, columns: list, key: str) -> None:
        """Show the form."""
        st.write(f"##### Settings for {self.__str__()} | [doc]({self.documentation_url()})")
        col1, col2 = st.columns(2)
        with col1:
            st.write("General options:")
            self.general_form(columns=columns, key=key)
        with col2:
            st.write("Extra options:")
            self.specific_form(key=key)

    def general_form(self, columns: list, key: str) -> None:
        """Show general plot options."""
        # self.y_axis = st.selectbox("Select a y-axis", options=[None] + columns, key=f"abscissa_col_{key}")
        self.color = st.selectbox("Select a color field", options=[None] + columns, key=f"color_col_{key}")
        self.log_x = st.selectbox(
            "Activate log scaling for the x-axis",
            options=[False, True],
            key=f"log_x_{key}",
        )
        self.log_y = st.selectbox(
            "Activate log scaling for the y-axis",
            options=[False, True],
            key=f"log_y_{key}",
        )
        self.orientation = st.selectbox(
            "Choose the orientation:",
            options=[None, "h", "v"],
            key=f"orientation_{key}",
        )

    @abc.abstractmethod
    def specific_form(self, key: str) -> None:
        """Show the specific form."""
        pass

    @abc.abstractmethod
    def show() -> None:
        """Show the plot in the streamlit webapp."""
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        """Return the name of the plot."""
        pass

    @abc.abstractmethod
    def documentation_url(self) -> str:
        """Return the documentation url of the plot."""
        pass


class Scatter(Plot):
    """Class containing the settings for scatter plots."""

    def __init__(self, columns: list, key: str):
        """Construct the scatter plot settings."""
        super().__init__(columns, key)
        # self.form.form_submit_button(label="Submit")

    def specific_form(self, key: str) -> None:
        """Show the specific settings for the scatter plot."""
        pass

    def show(self, df: pd.DataFrame, x_axis: str, y_axis: str) -> None:
        """Show the scatter plot in the streamlit webapp."""
        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            color=self.color,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=x_axis, selected_y=y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Scatter"

    def documentation_url(self) -> str:
        """Return the documentation url of the plot."""
        return "https://plotly.com/python-api-reference/generated/plotly.express.scatter.html"


class Histogram(Plot):
    """Class containing the settings for the histogram plot."""

    def __init__(self, columns: list, key: str):
        """Construct the histogram plot settings."""
        super().__init__(columns, key)

    def specific_form(self, key: str) -> None:
        """Show the specific settings for the histogram plot."""
        self.histnorm = st.selectbox(
            "Select a normalization",
            options=[None, "percent", "probability", "density"],
            key=f"histnorm_{key}",
        )
        self.histfunc = st.selectbox(
            "Select an aggregation function",
            options=[None, "count", "sum", "min", "max", "avg"],
            key=f"histfunc_{key}",
        )
        self.nbins = st.selectbox(
            "Select the number of bins",
            options=[None, 3, 5, 10, 20, 30, 50, 100, 200, 300, 500],
            key=f"nbins_{key}",
        )
        self.marginal = st.selectbox(
            "Select a marginal",
            options=[None, "rug", "box", "violin", "histogram"],
            key=f"marginal_{key}",
        )

    def show(self, df: pd.DataFrame, x_axis: str, y_axis: str) -> None:
        """Show the histogram in the streamlit webapp."""
        fig = px.histogram(
            df,
            x=x_axis,
            y=y_axis,
            color=self.color,
            barmode="group",
            histfunc=self.histfunc,
            histnorm=self.histnorm,
            nbins=self.nbins,
            marginal=self.marginal,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=x_axis, selected_y=y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Histogram"

    def documentation_url(self) -> str:
        """Return the documentation url of the plot."""
        return "https://plotly.com/python-api-reference/generated/plotly.express.histogram.html"


class Box(Plot):
    """Class containing the settings for box plots."""

    def __init__(self, columns: list, key: str):
        """Constuct the box plot settings."""
        super().__init__(columns, key)

    def specific_form(self, key: str) -> None:
        """Show the specific settings for the box plot."""
        self.selected_points = st.selectbox(
            "Select how to display outliers",
            options=[
                None,
                "outliers",
                "suspectedoutliers",
                "all",
                False,
            ],
            key=f"selected_points_{key}",
        )

    def show(self, df: pd.DataFrame, x_axis: str, y_axis: str) -> None:
        """Show the box plot in the streamlit webapp."""
        fig = px.box(
            df,
            x=x_axis,
            y=y_axis,
            color=self.color,
            points=self.selected_points,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=x_axis, selected_y=y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Box"

    def documentation_url(self) -> str:
        """Return the documentation url of the plot."""
        return "https://plotly.com/python-api-reference/generated/plotly.express.box.html"


class Line(Plot):
    """Class containing the settings for line plot."""

    def __init__(self, columns: list, key: str):
        """Construct the line plot settings."""
        super().__init__(columns, key)
        # self.form.form_submit_button(label="Submit")

    def show(self, df: pd.DataFrame, x_axis: str, y_axis: str) -> None:
        """Show a line plot in the streamlit webapp."""
        fig = px.line(
            df,
            x=x_axis,
            y=y_axis,
            color=self.color,
            log_x=self.log_x,
            log_y=self.log_y,
            category_orders=determine_category_order(selected_col=x_axis, selected_y=y_axis, df=df),
            orientation=self.orientation,
        )
        st.plotly_chart(fig, use_container_width=True)

    def __str__(self) -> str:
        """Return the name of the plot."""
        return "Line"

    def documentation_url(self) -> str:
        """Return the documentation url of the plot."""
        return "https://plotly.com/python-api-reference/generated/plotly.express.line.html"


def determine_category_order(selected_col: str, selected_y: str, df: pd.DataFrame) -> dict:
    """Determine the category order for the plotly figure."""
    category_order = {selected_col: list(df[selected_col].value_counts().index)}
    if selected_y:
        category_order[selected_y] = list(df[selected_y].value_counts().index)
    return category_order
