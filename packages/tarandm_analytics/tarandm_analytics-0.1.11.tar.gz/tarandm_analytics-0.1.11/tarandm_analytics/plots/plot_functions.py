import uuid
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, model_validator


class PlotLibrary(str, Enum):
    PLT = "PLT"
    SHAP = "SHAP"


class PlotType(str, Enum):
    BAR = "BAR"
    WATERFALL = "WATERFALL"
    PLOT = "PLOT"


class IndividualPlot(BaseModel):
    plot_type: PlotType
    kwargs: Optional[Dict] = {}
    args: Optional[List] = []
    xlabel: Optional[str] = None
    ylabel: Optional[str] = None
    title: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def backwards_compatibility_plot_data(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "plot_data" in data:
                plot_data = data.pop("plot_data")
                data["kwargs"] = plot_data
        return data

    def model_dump(self, **kwargs: Any) -> Dict[str, Any]:
        # configure parent method
        kwargs.setdefault("exclude_none", True)
        kwargs.setdefault("exclude_defaults", True)
        return super().model_dump(**kwargs)

    def plot(self, plot_library: PlotLibrary, fig: "matplotlib.pyplot.Figure") -> None:
        import shap
        import numpy as np

        shap_plot_function_mapping = {"WATERFALL": shap.plots.waterfall}
        plt_plot_function_mapping = {"PLOT": fig.gca().plot, "BAR": fig.gca().bar}

        plot_type = self.plot_type
        kwargs = self.kwargs
        args = self.args

        if plot_library == "SHAP":
            shap_values = shap._explanation.Explanation(
                values=np.array(kwargs["values"]),
                base_values=kwargs["base_value"],
                data=np.array(kwargs["data"]),
                feature_names=kwargs["feature_names"],
            )

            shap_plot_function_mapping[plot_type](shap_values, show=False)

        elif plot_library == "PLT":
            from matplotlib.ticker import ScalarFormatter

            if "color" not in kwargs:
                kwargs["color"] = "#0eab9c"

            plt_plot_function_mapping[plot_type](*args, **kwargs)

            fig.gca().spines["top"].set_visible(False)
            fig.gca().spines["right"].set_visible(False)

            fig.gca().spines["left"].set_color("#515353")
            fig.gca().spines["bottom"].set_color("#515353")

            # Create a ScalarFormatter object
            formatter = ScalarFormatter(useOffset=False)
            formatter.set_scientific(False)
            formatter.set_useOffset(False)

            # Apply the formatter to the x-axis and y-axis
            fig.gca().xaxis.set_major_formatter(formatter)
            fig.gca().yaxis.set_major_formatter(formatter)

            for axis in fig.axes:
                if self.title:
                    axis.set_title(self.title)
                if self.xlabel:
                    axis.set_xlabel(self.xlabel, color="#515353")
                if self.ylabel:
                    axis.set_ylabel(self.ylabel, color="#515353")

            fig.gca().tick_params(axis="x", colors="#515353")
            fig.gca().tick_params(axis="y", colors="#515353")

        else:
            raise ValueError(f"Unknown plot library {plot_library}")


class PlotData(BaseModel):
    plot_name: str
    plot_library: PlotLibrary
    plot_content: List[IndividualPlot]

    def create_plot(self) -> "matplotlib.pyplot.Figure":
        from matplotlib import pyplot as plt

        plot_library = self.plot_library
        plot_content = self.plot_content

        fig = plt.figure(num=str(uuid.uuid4()))
        for individual_plot in plot_content:
            individual_plot.plot(plot_library=plot_library, fig=fig)

        return fig
