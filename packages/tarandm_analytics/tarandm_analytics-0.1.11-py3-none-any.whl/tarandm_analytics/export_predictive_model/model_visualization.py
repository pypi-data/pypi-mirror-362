from io import BytesIO
from typing import Optional, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd
    from xgboost import Booster
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier

import structlog


logger = structlog.get_logger(__name__)


def shap_summary_plot_logistic_regression(model: "LogisticRegression", data: "pd.DataFrame") -> BytesIO:
    import shap
    import matplotlib.pyplot as plt

    attributes = model.feature_names_in_
    masker = shap.maskers.Independent(data=data[attributes])
    explainer = shap.LinearExplainer(model, masker=masker)
    shap_values = explainer.shap_values(data[attributes])

    shap.summary_plot(
        shap_values,
        data[attributes],
        max_display=20,
        show=False,
        plot_type="bar",
    )

    ax = plt.gca()
    ax.tick_params(labelsize=14)
    ax.set_xlabel("mean(|SHAP value|) (average impact on model output magnitude)", fontsize=10)

    if ax.get_legend():
        ax.get_legend().remove()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="svg", bbox_inches="tight")
    plt.close()

    return image_stream


def shap_summary_plot_xgboost(model: "Booster", data: "pd.DataFrame") -> BytesIO:
    import shap
    import matplotlib.pyplot as plt

    attributes = model.feature_names
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data[attributes])
    shap.summary_plot(shap_values, data[attributes], max_display=20, show=False)

    ax = plt.gca()
    if ax.get_legend():
        ax.get_legend().remove()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="svg", bbox_inches="tight")
    plt.close()

    return image_stream


def learning_curves_plot(model: "Booster", evaluations_result: Dict, metric: Optional[str] = None) -> BytesIO:
    import matplotlib.pyplot as plt

    if metric is None:
        metric_final = list(evaluations_result[list(evaluations_result.keys())[0]].keys())[0]
        logger.info(
            f"Learning curves plot: Metric to be plotted was not provided. Automatically assigned metric '{metric_final}'."
        )
    # elif metric not in evaluations_result
    else:
        metric_final = metric

    total_iteration_count = len(evaluations_result[list(evaluations_result.keys())[0]][metric_final])
    best_score = getattr(model, "best_score", None)
    best_iteration = getattr(model, "best_iteration", None)
    taran_rgb = (10 / 255, 134 / 255, 132 / 255)

    ax = plt.subplot(1, 1, 1)
    for sample, vals in evaluations_result.items():
        ax.plot(range(1, total_iteration_count + 1), vals[metric_final], label=sample)

    if best_score:
        ax.plot(
            [1, total_iteration_count],
            [best_score, best_score],
            color="black",
            ls="--",
            lw=1,
        )

        ax.scatter([best_iteration + 1], [best_score], color="black")
        ax.annotate(
            "{:d}; {:0.3f}".format(best_iteration, best_score),
            xy=(best_iteration + 1, best_score),
            xytext=(best_iteration + 1, best_score + 0.005),
        )

    ax.set_xlabel("ITERATION", color="gray")
    ax.set_ylabel(metric_final.upper(), color="gray")
    ax.set_title(f"Model training - {metric_final} curves", color=taran_rgb)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(taran_rgb)
    ax.spines["bottom"].set_color(taran_rgb)
    ax.tick_params(axis="y", colors="gray")
    ax.tick_params(axis="x", colors="gray")
    ax.legend(loc="best")

    image_stream = BytesIO()
    plt.savefig(image_stream, format="svg")
    plt.close()

    return image_stream


def shap_summary_plot_random_forest(
    model: "RandomForestClassifier",
    data: "pd.DataFrame",
    target_class: Optional[str],
) -> BytesIO:
    import shap
    import matplotlib.pyplot as plt

    class_index = [str(c) for c in model.classes_].index(target_class)
    attributes = model.feature_names_in_

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data[attributes])

    shap.summary_plot(
        [shap_values[class_index]],
        data[attributes],
        max_display=20,
        show=False,
        class_names=[f"Target: {target_class}"],
    )

    ax = plt.gca()
    ax.tick_params(labelsize=14)
    ax.set_xlabel("mean(|SHAP value|) (average impact on model output magnitude)", fontsize=12)
    if ax.get_legend():
        ax.get_legend().remove()

    image_stream = BytesIO()
    plt.savefig(image_stream, format="svg", bbox_inches="tight")
    plt.close()

    return image_stream
