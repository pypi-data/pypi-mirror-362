import base64
import datetime
import importlib
import io
import pickle
import zipfile
from typing import List, Dict, Union, Optional, Any, Tuple, TYPE_CHECKING

import requests
import structlog

if TYPE_CHECKING:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.tree._tree import Tree
    from xgboost import Booster
    import pandas as pd
    import numpy as np
else:
    RandomForestClassifier = Any
    LogisticRegression = Any
    DecisionTreeClassifier = Any
    Booster = Any

from path import Path
from requests.auth import HTTPBasicAuth
import os

from tarandm_analytics.export_predictive_model.model_visualization import (
    shap_summary_plot_logistic_regression,
    shap_summary_plot_xgboost,
    shap_summary_plot_random_forest,
    learning_curves_plot,
)
from tarandm_analytics.base_class import TaranDMAnalytics
from tarandm_analytics.utils import get_number_formatting

logger = structlog.get_logger(__name__)


class ExportPredictiveModel(TaranDMAnalytics):
    def __init__(
        self,
        endpoint_url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        skip_endpoint_validation: bool = False,
    ):
        super().__init__(
            endpoint_url=endpoint_url,
            username=username,
            password=password,
            skip_endpoint_validation=skip_endpoint_validation,
        )
        if not skip_endpoint_validation:
            self.supported_model_types = self.get_supported_model_types()
        else:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.linear_model import LogisticRegression
            from xgboost import Booster
            from sklearn_pmml_model.linear_model import PMMLLogisticRegression
            from sklearn_pmml_model.ensemble import PMMLForestClassifier
            from sklearn_pmml_model.ensemble.gb import PMMLGradientBoostingClassifier

            self.supported_model_types = {
                "LOGISTIC_REGRESSION": LogisticRegression,
                "XGB": Booster,
                "EXPERT_SCORE": None,
                "RANDOM_FOREST": RandomForestClassifier,
                "PMML": [PMMLLogisticRegression, PMMLForestClassifier, PMMLGradientBoostingClassifier],
            }

    def validate_analytics_url(self) -> None:
        # TODO: define info endpoint in analytics and call it here
        pass

    def get_supported_model_types(self) -> Dict[str, Any]:
        """
        Fetch predictive model types supported by TaranDM.

        :return: Dictionary with model_type as key, related python class as value.
        """
        url = self.endpoint_url + "analytics/supported_predictive_models"
        response = requests.get(url=url, auth=HTTPBasicAuth(self.username, self.password))
        supported_models = {}

        if response.status_code == 200:
            logger.info(
                "Supported predictive model types were extracted from 'analytics/supported_predictive_models' "
                "endpoint."
            )
            response_data = response.json()

            for predictive_model_type, predictive_model_class_str in response_data.items():
                if predictive_model_class_str == "None":
                    supported_models[predictive_model_type] = None
                elif isinstance(predictive_model_class_str, list):
                    try:
                        supported_models[predictive_model_type] = []
                        for class_str in predictive_model_class_str:
                            module_str, class_name = class_str.rsplit(".", 1)
                            module = importlib.import_module(module_str)
                            predictive_model_class = getattr(module, class_name)
                            supported_models[predictive_model_type].append(predictive_model_class)
                    except (ModuleNotFoundError, AttributeError) as e:
                        logger.warning(
                            f"Unable to import class {predictive_model_class_str} connected with "
                            f"{predictive_model_type} predictive model type: {e}"
                        )
                        supported_models[predictive_model_type] = None
                else:
                    try:
                        module_str, class_name = predictive_model_class_str.rsplit(".", 1)
                        module = importlib.import_module(module_str)
                        predictive_model_class = getattr(module, class_name)
                        supported_models[predictive_model_type] = predictive_model_class
                    except (ModuleNotFoundError, AttributeError) as e:
                        logger.warning(
                            f"Unable to import class {predictive_model_class_str} connected with "
                            f"{predictive_model_type} predictive model type: {e}"
                        )
                        supported_models[predictive_model_type] = None
        else:
            logger.warning(
                "Unable to extract supported predictive model types from "
                "'analytics/supported_predictive_models' endpoint."
            )

        return supported_models

    def prepare_predictive_model_data(
        self,
        model: Union[
            "LogisticRegression", "RandomForestClassifier", "Booster", "pd.DataFrame", "pl.DataFrame", io.StringIO
        ],
        attributes: Optional[List[str]] = None,
        model_name: Optional[str] = None,
        model_type: Optional[str] = None,
        data: Optional["pd.DataFrame"] = None,
        label_name: Optional[str] = None,
        target_class: Optional[str] = None,
        attribute_binning: Optional[Dict] = None,
        attribute_transformation: Optional[Union[Dict[str, str], List[Dict[str, str]]]] = None,
        dummy_encoding: Optional[
            Union[
                List[Dict[str, Union[str, Dict[str, Union[str, bool]]]]], Dict[str, List[Dict[str, Union[str, bool]]]]
            ]
        ] = None,
        monitoring_data: Optional[Dict[str, List[Dict]]] = None,
        hyperparameters: Optional[Dict] = None,
        general_notes=None,
        attribute_description: Optional[Dict[str, str]] = None,
        column_name_sample: Optional[str] = None,
        column_name_date: Optional[str] = None,
        column_name_prediction: Optional[str] = None,
        evaluate_performance: Optional[Dict[str, Union[str, List[str]]]] = None,
        learning_curves_data: Optional[Dict] = None,
    ) -> Tuple[Dict[str, Any], Optional[List[Dict[str, Any]]]]:
        """
        Function prepares input data for build model zip file, that is ready to be implemented in TaranDM software.
        Created input data will be sent to the TaranDM endpoint, through which final model zip file is returned.

        :param model: Trained predictive model. One of from "sklearn.ensemble.RandomForestClassifier",
        "sklearn.linear_model.LogisticRegression", "xgboost.Booster", "pd.DataFrame". "pd.DataFrame" represents expert
        scorecard model, where user manually defines values for predictor bins.
        :param attributes: List of model predictors before transformation or binning. For example if 'age' is binned
        into 'age_binned' and binned version enters the model, list of predictors should include 'age' (rather than
        'age_binned') and binning for age should be provided in 'attribute_binning' parameter.
        :param model_name: Name of the model (will be visible in TaranDM GUI).
        :param model_type: Type of the model. One of "XGB", "LOGISTIC_REGRESSION", "RANDOM_FOREST", "EXPERT_SCORE".
        :param data: Dataset used for model training. Required to calculate model performance, and descriptive
        statistics about development sample. Should contain all the predictors as they enter the model (after binning).
        :param label_name: Name of the target variable. Should be included in data to properly evaluate model
        performance.
        :param target_class: Target class predicted by the model.
        :param attribute_binning: Attribute binning (if applied). In inference phase, we first apply predictor
        transformation (if defined), then binning and dummy encoding. Resulting value is passed to model predict method.

        Binning should be provided as a dictionary with following structure:
        binning = {
            'numerical_predictor1': {
                'dtype': 'NUMERICAL',
                'bins': [-np.inf, 20, 35, 50, np.inf],
                'bin_vals': [1, 2, 3, 4, 1000],
                'null_val': 0,
                'binned_attribute_name': 'name_after_binning'
            },
            'categorical_predictor1': {
                'dtype': 'CATEGORICAL',
                'bins': [['M'], ['F']]',
                'bin_vals': [1, 2, 3, 4, 1000],
                'null_val': 0
            },
            ...
        }
        Keys of provided dictionary are names of the predictors. TaranDM supports 'NUMERICAL' and 'CATEGORICAL' data
        types of predictors. For numerical predictors, binning is defined by providing list of bin borders. For
        categorical predictors, binning is defined by providing list of lists. Inner lists define values that belong
        to each group. Both 'NUMERICAL' and 'CATEGORICAL' data types contain attributes 'bin_vals' and
        'null_val'. Those are values used for encoding the bins. 'null_val' is an encoding value for null values
        (missings).

        :param attribute_transformation: Transformation of the predictors. Transformation is applied before binning. If
        both transformation and binning are defined, predictor is first transformed and binning is applied on values
        obtained after transformation.

        Transformation should be provided as a dictionary with following structure:
        transformation = {
            'numerical_predictor1': '{numerical_predictor1} + 1'
            ...
        }
        In transformation formula, anything in "{}" is considered as predictor and will be replaced with predictor value
        during formula evaluation.

        :param dummy_encoding: Dummy encoding of predictors. Following for is required:
        dummy_encoding = {
            'feature_name': [
                {
                    'value': 'first_value_to_be_encoded',
                    'encoded_feature_name': 'name_of_created_dummy_feature_val1',
                    'use_for_undefined': False
                },
                {
                    'value': 'second_value_to_be_encoded',
                    'encoded_feature_name': 'name_of_created_dummy_feature_val1',
                    'use_for_undefined': True
                },
            ]
        }
        'use_for_undefined' is a boolean value - if True, then created dummy variable will have value 1 for unknown
        values (values not defined in other dummies).
        :param monitoring_data: Data for monitoring, including attribute's binning with bin frequency and bin target
        rate. Those data are used in monitoring for evaluation of stability in time (PSI).
        :param hyperparameters: Model hyperparameters.
        :param general_notes: Dictionary of general notes about the model. Notes will be displayed in GUI.
        :param attribute_description: Dictionary with description of predictors.
        :param column_name_sample: Name of the column in data, that defines different data sample types (train, test,
        etc.). If provided, sample statistics will be stored in model metadata.
        :param column_name_date: Name of the column in data, that defines time dimension. If provided, information about
        time range used in development sample data will be stored in model metadata.
        :param column_name_prediction: Name of the column in data, that holds model prediction. This column is used to
        evaluate model performance.
        :param evaluate_performance: Dictionary that defines performance to be evaluated - which target and over which
        sample types. Use following structure:

        evaluate_performance = {
            'label_3M': 'AUC',
            'label_12M': ['AUC', 'GINI']
        }
        :param learning_curves_data: Data for plotting learning curves plot in following structure:

        learning_curves_data = {
            'sample1': {
                'metric1': [
                    0.5,
                    0.4,
                    0.3
                ]
            },
            'sample2': {
                'metric1': [
                    0.6,
                    0.5,
                    0.4
                ]
            }
        }
        :return:
        """
        import pandas as pd

        # 1. Restructure dummy encoding and transformations into new format if provided in old format
        dummy_encoding_formatted = self._format_dummy_encoding(dummy_encoding)
        transformations_formatted = self._format_transformations(attribute_transformation)

        # 2. Basic validations
        if model is None:
            raise ValueError("Parameter 'model' must contain predictive model to be exported. Provided value 'None'.")
        elif isinstance(model, pd.DataFrame):
            import polars as pl

            model = pl.from_pandas(model)

        model_type_final = self._validate_model_type(model_type, model)
        model_name_final = self._validate_model_name(model_name, model_type_final)
        if model_type_final == "PMML":
            # TODO: add validation that StringIO in model can be parsed?
            model_attributes_orig = attributes
        else:
            model_attributes_orig = self._validate_feature_names(
                attributes=attributes,
                transformations=transformations_formatted,
                attribute_binning=attribute_binning,
                dummy_encoding=dummy_encoding_formatted,
                model=model,
            )

        # 3. Serialize model
        serialized_model = self._get_dumped_model(model, model_type_final)
        if model_type_final == "PMML" and "feature_names" not in serialized_model:
            serialized_model["feature_names"] = attributes

        # 4. Get descriptive data about data samples used in model development
        sample_description_data = self._get_data_sample_description(
            data=data,
            column_name_label=label_name,
            column_name_sample=column_name_sample,
            column_name_date=column_name_date,
        )

        # 5. Get model performance over different samples
        model_performance = self._get_predictive_model_performance(
            data=data,
            column_name_sample=column_name_sample,
            column_name_prediction=column_name_prediction,
            evaluate_performance=evaluate_performance,
        )

        # 6. Generate images
        images, images_meta = self._generate_images(
            data=data,
            model=model,
            model_type=model_type_final,
            target_class=target_class,
            learning_curves_data=learning_curves_data,
        )

        # 7. Prepare request data
        request_data = {
            "model": serialized_model,
            "model_name": model_name_final,
            "model_type": model_type_final,
        }

        if model_attributes_orig:
            request_data["predictors"] = model_attributes_orig
        if general_notes:
            request_data["general_notes"] = general_notes
        if hyperparameters:
            request_data["hyperparameters"] = hyperparameters
        if label_name:
            request_data["label_name"] = label_name
        if target_class:
            request_data["target_class"] = str(target_class)
        if attribute_binning:
            request_data["attribute_binning"] = self._replace_inf_bin_borders(attribute_binning)
        if dummy_encoding:
            request_data["dummy_encoding"] = dummy_encoding_formatted
        if transformations_formatted:
            request_data["attribute_transformation"] = transformations_formatted
        if monitoring_data:
            request_data["monitoring_data"] = monitoring_data
        if attribute_description:
            request_data["attribute_description"] = attribute_description
        if sample_description_data:
            request_data["sample_description_data"] = sample_description_data
        if model_performance:
            request_data["model_performance"] = model_performance
        if images_meta:
            request_data["attached_images"] = images_meta

        return request_data, images

    def build_predictive_model(
        self, request_data: Dict[str, Any], filename: str, images: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Export predictive model as a zip file ready to import in TaranDM.

        :param request_data: Request data in the same form as output of `prepare_predictive_model_data` method. In fact,
        mentioned method provides a tuple, with request data on the first position and images on the second position.
        :param filename: File name of exported zip file
        :param images: Images to be exported with the model. Images are displayed in GUI with the model and they are
        returned by `prepare_predictive_model_data` method.
        :return:
        """
        extended_model_yaml, external_model_json, external_model_pmml, images = self._build_predictive_model(
            request_data=request_data, images=images
        )

        self.save_to_zip(
            extended_model_yaml=extended_model_yaml,
            filename=filename,
            external_model_json=external_model_json,
            external_model_pmml=external_model_pmml,
            images=images,
        )

        logger.info(f"Model was exported into {filename} file. It is ready for deployment in TaranDM.")

    def _build_predictive_model(
        self, request_data: Dict[str, Any], images: Optional[List[Dict[str, Any]]] = None
    ) -> Optional[Tuple[Any, Any, Any, List[Any]]]:
        if images is None:
            images = []
            attached_images = request_data.get("attached_images", [])
            if len(attached_images) > 0:
                request_data["attached_images"] = []
                logger.warning(
                    f"Provided metadata suggests that images should be attached, but not images were "
                    f"provided in function call. Images will not be attached to model."
                )

        url = self.endpoint_url + "analytics/build_predictive_model"
        response = requests.post(url=url, json=request_data, auth=HTTPBasicAuth(self.username, self.password))

        if response.status_code == 200:
            logger.info("Successfully called 'analytics/build_predictive_model' endpoint.")
            response_data = response.json()
        else:
            logger.error(f"Unable to call 'analytics/build_predictive_model' endpoint: {response.text}")
            return None
        extended_model_yaml = response_data["extended_predictive_model_yaml"]
        external_model_json = response_data.get("external_model_json")
        external_model_pmml = response_data.get("external_model_pmml")

        return extended_model_yaml, external_model_json, external_model_pmml, images

    @staticmethod
    def save_to_zip(
        extended_model_yaml: str,
        filename: str,
        external_model_json: Optional[str] = None,
        external_model_pmml: Optional[str] = None,
        images: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        if images is None:
            images = []

        def add_file(archive, buffer, name):
            if isinstance(buffer, io.StringIO):
                buffer.seek(0)
                buffer = io.BytesIO(buffer.read().encode())
            buffer.seek(0, os.SEEK_END)
            buffer.seek(0)
            archive.writestr(name, buffer.getvalue())

        out = io.BytesIO()
        with zipfile.ZipFile(file=out, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            add_file(zf, io.StringIO(extended_model_yaml), "extended_model.yaml")
            if external_model_json is not None:
                add_file(zf, io.StringIO(external_model_json), "external_model.json")
            elif external_model_pmml is not None:
                add_file(zf, io.StringIO(external_model_pmml), "external_model.pmml")
            else:
                raise ValueError("Both 'external_model_pmml' and 'external_model_json' are None.")
            for img in images:
                add_file(zf, img["image"], img["filename"])

        path = Path(filename)
        if not path.endswith(".zip"):
            path += ".zip"

        with open(path, "wb") as f:
            f.write(out.getbuffer())

    @staticmethod
    def _format_transformations(
        transformations: Optional[Union[Dict[str, str], List[Dict[str, str]]]],
    ) -> Optional[List[Dict[str, str]]]:
        if transformations is None:
            return None

        try:
            if isinstance(transformations, dict):
                transformations_formatted = []
                for attr, transformation in transformations.items():
                    transformations_formatted.append(
                        {
                            "attribute": attr,
                            "transformation": transformation,
                        }
                    )
                return transformations_formatted
            elif isinstance(transformations, list):
                # TODO: add validation of data in list
                return transformations
        except Exception:
            message = """
            Transformations were provided in incorrect format. We support two formats:
            example_transformation_format_1 = [
                {
                    "attribute": "age",
                    "transformation": "{age} * {age}"
                    "transformed_attribute_name": "age_squared"
                }
            ]

            example_transformation_format_2 = {
                "age": "{age} * {age}" # age squared values will rewrite values in age attribute
            }
            """
            raise ValueError(message)

    @staticmethod
    def _format_dummy_encoding(
        dummy_encoding: Optional[
            Union[
                List[Dict[str, Union[str, Dict[str, Union[str, bool]]]]], Dict[str, List[Dict[str, Union[str, bool]]]]
            ]
        ],
    ) -> Optional[List[Dict[str, Union[str, Dict[str, Union[str, bool]]]]]]:
        if dummy_encoding is None:
            return None

        try:
            if isinstance(dummy_encoding, dict):
                dummy_encoding_formatted = []
                for attr, enc in dummy_encoding.items():
                    dummy_encoding_formatted.append({"attribute": attr, "encoding": enc})
                return dummy_encoding_formatted
            elif isinstance(dummy_encoding, list):
                # TODO: add validation of data in list
                return dummy_encoding

        except Exception:
            message = """
            Dummy encoding was provided in incorrect format. We support two formats:
            example_encoding_format_1 = [
                {
                    "attribute": "education",
                    "encoding": [
                        {
                            "value": "UNIVERSITY",
                            "encoded_feature_name": "education_university",
                            "use_for_undefined": False
                        },
                        {
                            "value': 'HIGH_SCHOOL",
                            "encoded_feature_name": "education_high_school",
                            "use_for_undefined": True
                        },
                    ]
                }
            ]
            
            example_encoding_format_2 = {
                "education": [
                    {
                        "value": "UNIVERSITY",
                        "encoded_feature_name": "education_university",
                        "use_for_undefined": False
                    },
                    {
                        "value': 'HIGH_SCHOOL",
                        "encoded_feature_name": "education_high_school",
                        "use_for_undefined": True
                    },
                ]
            }
            """
            raise ValueError(message)

    @staticmethod
    def _replace_inf_bin_borders(grouping: Dict[str, Any]) -> Dict[str, Any]:
        import numpy as np

        grouping_transformed = {}
        for attr, binning in grouping.items():
            grouping_transformed[attr] = binning
            if binning["dtype"] == "NUMERICAL":
                bin_borders = []
                for border in binning["bins"]:
                    if border == -np.inf:
                        bin_borders.append(-987654321.987654321)
                    elif border == np.inf:
                        bin_borders.append(987654321.987654321)
                    else:
                        bin_borders.append(border)
                grouping_transformed[attr]["bins"] = bin_borders
        return grouping_transformed

    @staticmethod
    def _evaluate_auc(label, prediction) -> Optional[float]:
        if len(set(label)) == 1:
            logger.warning(
                "Evaluating model AUC: Only one class present in y_true. ROC AUC score is not defined in " "that case"
            )
            return None
        elif len(set(label)) > 2:
            logger.warning(
                f"Evaluating model AUC: AUC evaluation supports only binary labels. Provided label contains "
                f"{len(set(label))} unique values."
            )
            return None

        from sklearn.metrics import roc_auc_score

        try:
            return roc_auc_score(y_true=label, y_score=prediction)
        except Exception as e:
            logger.warning(f"Evaluating model AUC: Failed to evaluate 'roc_auc_score' function with error: {e}.")
            return None

    def _evaluate_gini(self, label, prediction) -> Optional[float]:
        auc = self._evaluate_auc(label, prediction)
        if auc is None:
            return None
        else:
            return 2 * self._evaluate_auc(label, prediction) - 1

    def _get_predictive_model_performance(
        self,
        data: Optional["pd.DataFrame"],
        column_name_sample: Optional[str],
        column_name_prediction: str,
        evaluate_performance: Dict[str, Union[str, List[str]]],
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Function calculates different performance metrics of predictive model.

        :param data: Dataset to be used for evaluating performance.
        :param column_name_sample: Name of the column inside 'data' that distinguishes type of data samples. Column can
               contain for instance values 'train', 'valid', 'test'. This will define which observations belong to train
               set, validation set and test set.
        :param column_name_prediction: Name of the column inside 'data' that holds values of predictive model prediction.
        :param evaluate_performance: Dictionary that defines what metrics should be evaluated. Keys in dictionary must refer
               to columns in 'data' that will be used as true label. Multiple true label columns can be defined. This can be
               useful for instance in situations when we have binary labels (indicators of an event) calculated over
               different time windows. In values under each key, metrics to be evaluated are defined.

               Example:
               evaluate_performance = {
                   'label_3M': 'AUC',
                   'label_12M': ['AUC', 'GINI']
               }
        :return: Dictionary with calculated performance metrics.
        """
        if evaluate_performance is None:
            logger.info("No performance metrics were requested for evaluation.")
            return None

        if data is None:
            logger.warning(
                "Preparing model performance data: No dataset was provided. Cannot evaluate model " "performance."
            )
            return None
        if len(data) == 0:
            logger.warning(
                "Preparing model performance data: Provided dataset has 0 observations. Cannot evaluate "
                "model performance."
            )
            return None

        message_common_part = (
            "Evaluating model performance: To evaluate model performance, provided dataset "
            "should contain a column with generated model predictions. Name of prediction column "
            "should be provided through 'column_name_prediction' parameter of "
            "'prepare_predictive_model_data' method."
        )
        if column_name_prediction is None:
            logger.warning(
                f"{message_common_part} 'column_name_prediction' was not provided. Cannot evaluate model performance."
            )
            return None

        if column_name_prediction not in data.columns:
            logger.warning(
                f"{message_common_part} Provided name of the column that holds predictions ('{column_name_prediction}')"
                f" is not in provided dataset. Cannot evaluate model performance."
            )
            return None

        if column_name_sample is None:
            logger.warning(
                "Evaluating model performance: Column name with sample type was not provided. All observations will be "
                "treated as training data."
            )
            column_name_sample = self._generate_sample_type_column_name(data=data)
            data[column_name_sample] = "train"
        elif column_name_sample not in data.columns:
            logger.warning(
                f"Evaluating model performance: Provided column name with sample type '{column_name_sample}' does not "
                f"exist in data. All observations will be treated as training data."
            )
            # _generate_sample_type_column_name makes sure that it does not overwrite existing column
            column_name_sample = self._generate_sample_type_column_name(data=data)
            data[column_name_sample] = "train"

        implemented_performance_metrics = {"AUC": self._evaluate_auc, "GINI": self._evaluate_gini}

        performance = []
        included_sample_types = data[column_name_sample].unique()
        for label, metrics in evaluate_performance.items():
            if isinstance(metrics, str):
                metrics = [metrics]

            for sample in included_sample_types:
                mask = data[column_name_sample] == sample
                performance_by_metric = {}
                for metric in metrics:
                    if metric.upper() not in implemented_performance_metrics:
                        logger.warning(
                            f"Evaluating model performance: Requested metric '{metric}' is not supported. Cannot "
                            f"evaluate '{metric}' for '{sample}' data sample. Supported performance metrices are: "
                            f"{', '.join(implemented_performance_metrics)}"
                        )
                        continue

                    if label not in data.columns:
                        logger.warning(
                            f"Evaluating model performance: Label '{label}' was not found in provided dataset. Cannot "
                            f"evaluate '{metric}' for '{sample}' data sample."
                        )
                        continue

                    evaluated_metric = implemented_performance_metrics[metric.upper()](
                        data[mask][label], data[mask][column_name_prediction]
                    )
                    if evaluated_metric is None:
                        continue
                    performance_by_metric[metric.upper()] = evaluated_metric

                if performance_by_metric:
                    performance.append(
                        {"target": label, "sample": sample.upper(), "performance": performance_by_metric}
                    )

        return performance if performance else None

    @staticmethod
    def _generate_sample_type_column_name(data: "pd.DataFrame") -> str:
        if "sample" not in data.columns:
            return "sample"
        else:
            for i in range(1, 10000):
                if f"sample_{i}" not in data.columns:
                    return f"sample_{i}"
        return "column_with_sample_type"

    def _get_data_sample_description(
        self,
        data: Optional["pd.DataFrame"],
        column_name_label: Optional[str] = None,
        column_name_sample: Optional[str] = None,
        column_name_date: Optional[str] = None,
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Function evaluates different descriptive information about model development data sample, such as what time range
        was used, what are the frequencies of label classes and other.

        :param data: Dataset to be used for descriptive info evaluation.
        :param column_name_label: Name of the column inside 'data' that stores labels.
        :param column_name_sample: Name of the column inside 'data' that distinguishes type of data samples. Column can
               contain for instance values 'train', 'valid', 'test'. This will define which observations belong to train
               set, validation set and test set.
        :param column_name_date: Name of the column inside 'data' that stores dates related to observations.
        :return: Dictionary with descriptive info data.
        """
        if data is None:
            logger.warning(
                "Preparing sample descriptions: No dataset was provided. Cannot evaluate sample description " "data."
            )
            return None
        elif len(data) == 0:
            logger.warning(
                "Preparing sample descriptions: Provided dataset has 0 observations. Cannot evaluate sample "
                "description data."
            )
            return None

        if column_name_sample is None:
            logger.warning(
                "Preparing sample descriptions: Column name with sample type was not provided. All observations will "
                "be treated as training data."
            )
            # _generate_sample_type_column_name makes sure that it does not overwrite existing column
            column_name_sample = self._generate_sample_type_column_name(data=data)
            data[column_name_sample] = "train"
        elif column_name_sample not in data.columns:
            logger.warning(
                f"Preparing sample descriptions: Provided column name with sample type '{column_name_sample}' does not "
                f"exist in data. All observations will be treated as training data."
            )
            # _generate_sample_type_column_name makes sure that it does not overwrite existing column
            column_name_sample = self._generate_sample_type_column_name(data=data)
            data[column_name_sample] = "train"

        date_available = True
        if column_name_date is None:
            logger.warning(
                "Preparing sample descriptions: Date column name (parameter 'column_name_date') was not provided. Time "
                "related metadata will not be evaluated."
            )
            date_available = False
        elif column_name_date not in data.columns:
            logger.warning(
                f"Preparing sample descriptions: Provided date column name '{column_name_date}' does not exist in "
                f"data. Time related metadata will not be evaluated."
            )
            date_available = False
        elif data[column_name_date].dtype != "<M8[ns]":
            logger.warning(
                f"Preparing sample descriptions: Provided date column name '{column_name_date}' is of type "
                f"{data[column_name_date].dtype.__str__()}. Required type is '<M8[ns]'. Time related metadata will not "
                f"be evaluated."
            )
            date_available = False

        label_available = True
        label_binary = True
        if column_name_label is None:
            logger.warning(
                "Preparing sample descriptions: Label column name was not provided. Label related metadata "
                "will not be evaluated."
            )
            label_available = False
        elif column_name_label not in data.columns:
            logger.warning(
                f"Preparing sample descriptions: Provided label column name '{column_name_label}' does not exist in "
                f"data. Label related metadata will not be evaluated."
            )
            label_available = False
        elif data[column_name_label].nunique() != 2:
            label_binary = False

        included_sample_types = data[column_name_sample].unique()

        result = []
        for sample_type in included_sample_types:
            sample_meta = {"sample_type": sample_type.upper()}
            mask = data[column_name_sample] == sample_type
            sample_meta["number_of_observations"] = len(data[mask])

            if date_available:
                sample_meta["first_date"] = data[mask][column_name_date].min().strftime(format="%Y-%m-%d")
                sample_meta["last_date"] = data[mask][column_name_date].max().strftime(format="%Y-%m-%d")

            if label_available and label_binary:
                sample_meta["label_class_frequency"] = []
                for label_class in data[column_name_label].unique().tolist():
                    sample_meta["label_class_frequency"].append(
                        {
                            "label_class": label_class,
                            "number_of_observations": len(data[mask & (data[column_name_label] == label_class)]),
                        }
                    )
            result.append(sample_meta)

        return result

    def _get_model_type(self, model: Any) -> str:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.linear_model import LogisticRegression
        from xgboost import Booster
        import polars as pl

        if isinstance(model, io.StringIO):
            logger.info("Automatically added model type PMML.")
            return "PMML"
        elif isinstance(model, LogisticRegression):
            logger.info("Automatically assigned model type LOGISTIC_REGRESSION.")
            return "LOGISTIC_REGRESSION"
        elif isinstance(model, RandomForestClassifier):
            logger.info("Automatically added model type RANDOM_FOREST.")
            return "RANDOM_FOREST"
        elif isinstance(model, Booster):
            logger.info("Automatically added model type XGB.")
            return "XGB"
        elif isinstance(model, pl.DataFrame):
            logger.info("Automatically added model type EXPERT_SCORE.")
            return "EXPERT_SCORE"
        else:
            raise TypeError(
                f"Model type was not provided and neither could not be detected detected automatically. Available model "
                f"types are: {self.supported_model_types}"
            )

    @staticmethod
    def _generate_model_name(model_type: str) -> str:
        return f"{model_type.lower()}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    @staticmethod
    def _generate_images(
        data: "pd.DataFrame",
        model: Any,
        model_type: str,
        target_class: Optional[str] = None,
        learning_curves_data: Optional[Dict] = None,
    ) -> Tuple[Optional[List[Dict]], Optional[List[Dict]]]:
        images = []
        images_meta = []
        if data is None:
            logger.warning("Skipping shap summary plot - no data provided.")
            return None, None

        try:
            if model_type == "LOGISTIC_REGRESSION":
                img = shap_summary_plot_logistic_regression(model=model, data=data)
                images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
                images.append({"filename": "shap_summary.svg", "image": img})
            elif model_type == "XGB":
                img = shap_summary_plot_xgboost(model=model, data=data)
                images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
                images.append({"filename": "shap_summary.svg", "image": img})
            elif model_type == "RANDOM_FOREST":
                img = shap_summary_plot_random_forest(model=model, data=data, target_class=target_class)
                images_meta.append({"filename": "shap_summary.svg", "type": "shap_summary"})
                images.append({"filename": "shap_summary.svg", "image": img})
        except Exception as e:
            logger.warning(f"Failed to generate Shap summary plot: {e}")

        if model_type == "XGB":
            if learning_curves_data is None or len(learning_curves_data) == 0:
                logger.warning("Skipping learning curves plot - no data provided.")
            else:
                try:
                    img = learning_curves_plot(model=model, evaluations_result=learning_curves_data, metric=None)
                    images_meta.append({"filename": "learning_curves.svg", "type": "learning_curves"})
                    images.append({"filename": "learning_curves.svg", "image": img})
                except Exception as e:
                    logger.warning(f"Failed to generate learning curves plot: {e}")

        return images, images_meta

    def get_monitoring_data(
        self,
        data: "pd.DataFrame",
        attributes: List[str],
        label_name: str,
        model_output_name: Optional[str] = None,
        binning: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, List[Dict]]:
        """
        Method prepares monitoring data to be exported with the model. They are important for monitoring stability of
        predictors and predictions. Predictor binning can be provided. If not, then it is created automatically
        (using percentiles for numerical predictors and n most frequent categories for categorical predictors).

        :param data: Data used for creating binning and calculating bin frequency and target rate.
        :param attributes: Attributes for which monitoring data will be prepared.
        :param label_name: Name of the target column in `data`.
        :param model_output_name: Name of the column with model prediction. If provided, monitoring data for prediction
        are prepared.
        :param binning: Pre-defined binning. If provided, monitoring will use this binning instead of automatic binning.
        Should be of following form:
        binning = {
            'numerical_predictor1': {
                'dtype': 'NUMERICAL',
                'bins': [-np.inf, 20, 35, 50, np.inf],
                'bin_vals': [1, 2, 3, 4, 1000],
                'null_val': 0,
                'binned_attribute_name': 'name_after_binning'
            },
            'categorical_predictor1': {
                'dtype': 'CATEGORICAL',
                'bins': [['M'], ['F']]',
                'bin_vals': [1, 2, 3, 4, 1000],
                'null_val': 0
            },
            ...
        }
        :return: Dictionary with monitoring data.
        """

        if binning is None:
            binning = {}

        import pandas as pd

        monitoring_data = []
        for attr in attributes:
            if attr not in data.columns:
                logger.warning(
                    f"Attribute {attr} was not found in provided dataset. Skipping preparation of monitoring "
                    f"data for this attribute."
                )
            if pd.api.types.is_numeric_dtype(data[attr].dtype):
                monitoring_data.append(
                    self.create_numerical_attribute_binning(
                        data=data,
                        col_attribute=attr,
                        col_target=label_name,
                        bins=binning.get(attr, {}).get("bins", None),
                    )
                )
            else:
                monitoring_data.append(
                    self.create_categorical_attribute_binning(
                        data=data,
                        col_attribute=attr,
                        col_target=label_name,
                        categories=binning.get(attr, {}).get("categories", None),
                    )
                )

        model_output_monitoring_data = None
        if model_output_name is not None:
            if model_output_name not in data.columns:
                logger.warning(
                    f"Model output column {model_output_name} was not found in provided dataset. Skipping preparation of monitoring "
                    f"data for model output."
                )
            else:
                if pd.api.types.is_numeric_dtype(data[model_output_name].dtype):
                    model_output_monitoring_data = self.create_numerical_attribute_binning(
                        data=data,
                        col_attribute=model_output_name,
                        col_target=label_name,
                        bins=binning.get(model_output_name, {}).get("bins", None),
                        n_bins=10,
                    )
                else:
                    logger.warning(
                        f"Model output column {model_output_name} is expected to be numerical. Non-numerical type"
                        f"{data[model_output_name].dtype} was provided."
                    )

        return {"binning": monitoring_data, "predictive_model_output_binning": model_output_monitoring_data}

    def create_numerical_attribute_binning(
        self,
        data: "pd.DataFrame",
        col_attribute: str,
        col_target: str,
        n_bins: int = 7,
        bins: Optional[List[Union[int, float]]] = None,
    ) -> Dict[str, Any]:
        """Create attribute binning for monitoring purposes. Bins are established to contain similar share of population
        (based on percentiles).

        :param: data: Data sample to be used for binning creation.
        :param: col_attribute: Attribute's name.
        :param: col_target: Name of the target.
        :param: n_bins: Number of bins to be created.
        :return: AttributeBinning object
        """

        # for numerical attributes, n same frequent bins are defined
        attribute_binning = {"attribute": col_attribute, "attribute_data_type": "NUMERICAL"}
        import numpy as np

        if bins is None:
            if len(data[col_attribute].unique()) > n_bins:
                bins = list(
                    np.unique(
                        np.percentile(
                            data[data[col_attribute].notnull()][col_attribute], np.linspace(0, 100, n_bins + 1)
                        )
                    )
                )
                bins[0] = -np.inf
                bins[-1] = np.inf
            else:
                bins = sorted(data[col_attribute].unique().tolist())
                bins.insert(0, -np.inf)
                bins.append(np.inf)

        frequency_null, target_rate_null = self._get_numerical_bin_frequency_and_target_rate(
            data=data, col_attribute=col_attribute, col_target=col_target, lower_bound=None, upper_bound=None
        )
        attribute_bins = [
            {
                "type": "NUMERICAL",
                "lower_bound": None,
                "upper_bound": None,
                "frequency": 0.0,
                "target_rate": 0.0,
                "id": 0,
                "name": "0_default",
            },
            {
                "type": "NUMERICAL",
                "lower_bound": None,
                "upper_bound": None,
                "frequency": frequency_null,
                "target_rate": target_rate_null,
                "id": 1,
                "name": "1_null",
            },
        ]
        for i in range(len(bins) - 1):
            lower_bound = bins[i]
            upper_bound = bins[i + 1]

            if lower_bound == -np.inf:
                lower_bound_to_json = "-987654321.987654321"
            elif lower_bound == np.inf:
                lower_bound_to_json = "987654321.987654321"
            else:
                lower_bound_to_json = lower_bound

            if upper_bound == -np.inf:
                upper_bound_to_json = "-987654321.987654321"
            elif upper_bound == np.inf:
                upper_bound_to_json = "987654321.987654321"
            else:
                upper_bound_to_json = upper_bound

            frequency, target_rate = self._get_numerical_bin_frequency_and_target_rate(
                data=data,
                col_attribute=col_attribute,
                col_target=col_target,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )
            binning = {
                "type": "NUMERICAL",
                "lower_bound": lower_bound_to_json,
                "upper_bound": upper_bound_to_json,
                "frequency": frequency,
                "target_rate": target_rate,
                "id": i + 2,
                "name": f"{i + 2}_({get_number_formatting(lower_bound)};{get_number_formatting(upper_bound)})",
            }
            attribute_bins.append(binning)

        attribute_binning["attribute_binning"] = attribute_bins
        return attribute_binning

    def create_categorical_attribute_binning(
        self,
        data: "pd.DataFrame",
        col_attribute: str,
        col_target: str,
        n_bins: int = 7,
        categories: Optional[List[List[str]]] = None,
    ):
        """Create attribute binning for monitoring purposes. First n_bins - 1 most frequent categories will have
        separate bin, the remaining categories will be joint in another bin.

        :param: data: Data sample to be used for binning creation.
        :param: col_attribute: Attribute's name.
        :param: col_target: Name of the target.
        :param: n_bins: Number of bins to be created.
        :return: AttributeBinning object
        """

        # for numerical attributes, n same frequent bins are defined
        attribute_binning = {"attribute": col_attribute, "attribute_data_type": "CATEGORICAL"}

        if categories is None:
            categories_raw = [
                "null" if str(cat) == "nan" else cat
                for cat in data[col_attribute].value_counts(sort=True, ascending=False, dropna=True).index
            ]

            categories: List[List[str]] = []
            for i in range(min(n_bins - 1, len(categories_raw))):
                categories.append([categories_raw[i]])

            if len(categories_raw) >= n_bins:
                categories.append(categories_raw[n_bins:])

        frequency_null, target_rate_null = self._get_categorical_bin_frequency_and_target_rate(
            data=data, col_attribute=col_attribute, col_target=col_target, bin_categories=None
        )
        attribute_bins = [
            {"type": "CATEGORICAL", "categories": None, "frequency": 0, "target_rate": 0, "id": 0, "name": "0_default"},
            {
                "type": "CATEGORICAL",
                "categories": ["null"],
                "frequency": frequency_null,
                "target_rate": target_rate_null,
                "id": 1,
                "name": "1_null",
            },
        ]
        for i in range(len(categories)):
            frequency, target_rate = self._get_categorical_bin_frequency_and_target_rate(
                data=data, col_attribute=col_attribute, col_target=col_target, bin_categories=categories[i]
            )

            categories_str = ",".join(categories[i])
            binning = {
                "type": "CATEGORICAL",
                "categories": categories[i],
                "frequency": frequency,
                "target_rate": target_rate,
                "id": i + 2,
                "name": f"{i + 2}_{{{categories_str}}}",
            }
            attribute_bins.append(binning)

        attribute_binning["attribute_binning"] = attribute_bins
        return attribute_binning

    @staticmethod
    def _get_numerical_bin_frequency_and_target_rate(
        data: "pd.DataFrame",
        col_attribute: str,
        col_target: str,
        lower_bound: Optional[Union[int, float]],
        upper_bound: Optional[Union[int, float]],
    ) -> Tuple[Optional[float], Optional[float]]:
        """Calculate frequency and target rate for given bin of numerical attribute.

        :param: data: Data for calculating bin frequencies and respective target rate.
        :param: col_attribute: Name of the attribute.
        :param: col_target: Name of the target.
        :param: lower_bound: Lower bound of a bin.
        :param: upper_bound: Upper bound of a bin.
        :return:
        """
        total_count = len(data)
        if total_count == 0:
            logger.warning(
                f"Cannot calculate bin frequency and target rate for {col_attribute}. Provided data contains "
                f"no observations."
            )
            return None, None

        if lower_bound is None and upper_bound is None:
            mask_bin = data[col_attribute].isnull()
        else:
            mask_bin = (data[col_attribute] > lower_bound) & (data[col_attribute] <= upper_bound)

        bin_frequency = mask_bin.sum()
        bin_target_frequency = (mask_bin & (data[col_target] == 1)).sum()

        if bin_target_frequency == 0:
            if lower_bound is None and upper_bound is None:
                logger.info(f"Target rate for column {col_attribute} and bin 'null' is zero.")
            else:
                logger.info(f"Target rate for column {col_attribute} and bin ({lower_bound};{upper_bound}] is zero.")
            return bin_frequency / total_count, 0.0

        return bin_frequency / total_count, bin_target_frequency / bin_frequency

    @staticmethod
    def _get_categorical_bin_frequency_and_target_rate(
        data: "pd.DataFrame", col_attribute: str, col_target: str, bin_categories: Optional[List[str]]
    ) -> Tuple[Optional[float], Optional[float]]:
        """Calculate frequency and target rate for given bin of categorical attribute.

        :param: data: Data for calculating bin frequencies and respective target rate.
        :param: col_attribute: Name of the attribute.
        :param: col_target: Name of the target.
        :param: bin_categories: Categories included in bin.
        :return: Category frequency and target rate.
        """
        total_count = len(data)
        if total_count == 0:
            logger.warning(
                f"Cannot calculate bin frequency and target rate for {col_attribute}. Provided data contains "
                f"no observations."
            )
            return None, None

        if bin_categories is None:
            mask_bin = data[col_attribute].isnull()
            categories_str = "null"
        else:
            mask_bin = data[col_attribute].isin(bin_categories)
            categories_str = ",".join(bin_categories)

        bin_frequency = mask_bin.sum()
        bin_target_frequency = (mask_bin & (data[col_target] == 1)).sum()

        if bin_target_frequency == 0:
            if len(categories_str) > 30:
                categories_str = categories_str[0:27] + "..."
            logger.info(
                f"Target rate for predictor {col_attribute} and group of categories {{{categories_str}}} is zero."
            )
            return bin_frequency / total_count, 0.0

        return bin_frequency / total_count, bin_target_frequency / bin_frequency

    def _validate_model_type(
        self,
        model_type: Optional[str],
        model: Union["LogisticRegression", "RandomForestClassifier", "Booster", "pd.DataFrame"],
    ) -> str:
        if model_type is None:
            model_type_final = self._get_model_type(model=model)
        elif model_type not in self.supported_model_types.keys():
            logger.warning(
                f"Model type '{model_type}' is invalid. Supported model types are: "
                f"{', '.join(self.supported_model_types.keys())}. Will try to detect model type automatically."
            )
            model_type_final = self._get_model_type(model=model)
        else:
            model_type_final = model_type

        return model_type_final

    def _validate_model_name(self, model_name: Optional[str], model_type_final: str) -> str:
        if model_name is None:
            model_name_final = self._generate_model_name(model_type=model_type_final)
            logger.warning(f"Model name was not provided. Generated model name: '{model_name_final}'.")
        else:
            model_name_final = model_name

        return model_name_final

    def _validate_feature_names(
        self,
        attributes: Optional[List[str]],
        transformations: Optional[List[Dict[str, str]]],
        attribute_binning: Optional[Dict],
        dummy_encoding: Optional[List[Dict[str, Union[str, Dict[str, Union[str, bool]]]]]],
        model: Union["LogisticRegression", "RandomForestClassifier", "Booster", "pd.DataFrame"],
    ) -> Optional[List[str]]:
        model_attrs = self._get_feature_names_in(model)
        if model_attrs is None:
            return None

        # 1. First reverse attributes created in dummy encoding
        attrs_before_dummy_encoding = model_attrs.copy()
        if dummy_encoding:
            for encoding in dummy_encoding:
                attr = encoding["attribute"]
                for single_dummy in encoding["encoding"]:
                    encoded_feature_name = single_dummy["encoded_feature_name"]
                    if encoded_feature_name not in model_attrs:
                        logger.warning(
                            f"Dummy encoding for predictor {attr} defines feature {encoded_feature_name}. This "
                            f"feature is not used in model. Please check dummy encoding for typos."
                        )
                    else:
                        if attr not in attrs_before_dummy_encoding:
                            attrs_before_dummy_encoding.append(attr)
                        del attrs_before_dummy_encoding[attrs_before_dummy_encoding.index(encoded_feature_name)]

        # 2. Second, reverse attribute created in attribute binning
        attrs_before_binning = attrs_before_dummy_encoding.copy()
        if attribute_binning:
            for attribute, binning in attribute_binning.items():
                binned_attribute_name = binning.get("binned_attribute_name", None)
                if binned_attribute_name is not None and binned_attribute_name != attribute:
                    if binned_attribute_name not in attrs_before_dummy_encoding:
                        logger.warning(
                            f"Binning defines attribute '{binned_attribute_name}'. This feature is not used in model. "
                            f"Please check binning for typos."
                        )
                    else:
                        if attribute not in attrs_before_binning:
                            attrs_before_binning.append(attribute)
                        del attrs_before_binning[attrs_before_binning.index(binned_attribute_name)]

        # 3. Finally, reverse attributes created in transformations
        orig_attrs = attrs_before_binning.copy()
        if transformations:
            for transformation in transformations:
                transformed_attribute_name = transformation.get("transformed_attribute_name", None)
                original_attribute_name = transformation.get("attribute", None)
                if transformed_attribute_name is not None and transformed_attribute_name != original_attribute_name:
                    if (
                        transformed_attribute_name not in attrs_before_binning
                        and transformed_attribute_name not in attrs_before_dummy_encoding
                        and transformed_attribute_name not in model_attrs
                    ):
                        logger.warning(
                            f"Transformations defines attribute '{transformed_attribute_name}'. This feature is not "
                            f"used in model or later phases attribute preprocessing (binning and dummy encoding). "
                            f"Please check transformations for typos."
                        )
                    else:
                        if original_attribute_name not in orig_attrs:
                            orig_attrs.append(original_attribute_name)
                        del orig_attrs[orig_attrs.index(transformed_attribute_name)]

        if attributes is None:
            logger.info(f"Expected original features (features before transformation and encodings) are: {orig_attrs}.")
        elif set(attributes) != set(orig_attrs):
            logger.warning(
                f"Expected original features (features before transformation and encodings) are different "
                f"from predictors provided in 'attributes' parameter. Expected: {orig_attrs};   Provided: "
                f"{attributes}. Expected original features will be used in exported model. Please check "
                f"that this is a correct behavior."
            )

        return orig_attrs

    @staticmethod
    def _get_feature_names_in(model) -> Optional[List[str]]:
        from xgboost import Booster
        import polars as pl

        if isinstance(model, Booster):
            return list(model.feature_names)
        elif isinstance(model, pl.DataFrame):
            return None
        else:
            if hasattr(model, "feature_names_in_"):
                return list(model.feature_names_in_)
            else:
                raise ValueError(
                    "Unable to detect feature names that enters the model. Please add property "
                    "'feature_names_in_' to your model object. 'feature_names_in_' will contain names of "
                    "features as they enter the model, i.e. after applying transformations, encodings and "
                    "dummy encodings."
                )

    def _get_dumped_model(self, model: Any, model_type: str) -> Union[str, Dict[str, Any]]:
        if model_type == "PMML":
            return self.pmml_model_dump(model)
        elif model_type == "LOGISTIC_REGRESSION":
            return self.logreg_model_dump(model)
        elif model_type == "XGB":
            return self.xgb_model_dump(model)
        elif model_type == "EXPERT_SCORE":
            model_binary = pickle.dumps(model)
            model_binary_encoded = base64.b64encode(model_binary)
            model_binary_encoded_string = model_binary_encoded.decode("ascii")

            return model_binary_encoded_string
        elif model_type == "RANDOM_FOREST":
            return self.random_forest_model_dump(model)
        return {}

    @staticmethod
    def logreg_model_dump(model) -> Dict[str, Any]:
        import sklearn

        result = {"type": "LOGISTIC_REGRESSION", "package_version": sklearn.__version__}
        if model is not None:
            result["package"] = str(model.__class__)
            result["feature_names"] = list(model.feature_names_in_)
            result["init_params"] = model.get_params()
            result["logreg_model_params"] = mp = {}
            for p in ("coef_", "intercept_", "classes_", "n_iter_"):
                mp[p] = getattr(model, p).tolist()

        return result

    @staticmethod
    def xgb_model_dump(model) -> Dict[str, Any]:
        import xgboost as xgb
        import json

        result = {"type": "XGB", "package_version": xgb.__version__}
        if model is not None:
            result["feature_names"] = list(model.feature_names)
            result["package"] = str(model.__class__)
            result["xgb_model"] = json.loads(model.save_raw(raw_format="json").decode("utf-8"))
        return result

    def random_forest_model_dump(self, model) -> Dict[str, Any]:
        import sklearn

        result = {"type": "RANDOM_FOREST", "package_version": sklearn.__version__}
        if model is not None:
            result["feature_names"] = list(model.feature_names_in_)
            result["package"] = str(model.__class__)
            result["random_forest_model"] = self._random_forest_to_dict(model)

        return result

    @staticmethod
    def pmml_model_dump(model: io.StringIO) -> Dict[str, Any]:
        import sklearn_pmml_model

        result = {"type": "PMML", "package_version": sklearn_pmml_model.__version__}
        if model is not None:
            result["pmml_model"] = base64.b64encode(model.getvalue().encode()).decode("ascii")

            return result

    def _random_forest_to_dict(self, random_forest: "RandomForestClassifier") -> Dict[str, Any]:
        random_forest_dict = random_forest.__getstate__()

        random_forest_dict["classes_"] = [str(cl) for cl in random_forest_dict["classes_"]]
        random_forest_dict["estimators_"] = [self._decision_tree_to_dict(e) for e in random_forest_dict["estimators_"]]
        random_forest_dict["estimator_params"] = list(random_forest_dict["estimator_params"])

        if "feature_names_in_" in random_forest_dict:
            random_forest_dict["feature_names_in_"] = list(random_forest_dict["feature_names_in_"])

        remove_keys = ["estimator", "_estimator", "estimator_"]
        for remove_key in remove_keys:
            if remove_key in random_forest_dict:
                del random_forest_dict[remove_key]

        return random_forest_dict

    def _decision_tree_to_dict(self, decision_tree: "DecisionTreeClassifier") -> Dict[str, Any]:
        decision_tree_dict = decision_tree.__getstate__()

        decision_tree_dict["tree_"] = self._tree_to_dict(decision_tree.tree_)
        decision_tree_dict["classes_"] = decision_tree_dict["classes_"].astype(str).tolist()
        decision_tree_dict["n_classes_"] = int(decision_tree_dict["n_classes_"])

        if "_sklearn_version" in decision_tree_dict.keys():
            del decision_tree_dict["_sklearn_version"]

        return decision_tree_dict

    def _tree_to_dict(self, tree: "Tree") -> Dict[str, Any]:
        # TODO - resolve base_estimator, drop it somehow ...
        tree_dict = tree.__getstate__()

        tree_dict["nodes_types"] = self._get_structured_nparray_types(tree_dict["nodes"])
        tree_dict["nodes_values"] = tree_dict["nodes"].tolist()
        tree_dict["values"] = tree_dict["values"].tolist()

        # compatibility for  scikit <1.3
        from packaging import version
        import sklearn

        if version.parse(sklearn.__version__) < version.parse("1.4.0"):
            if "missing_go_to_left" not in tree_dict["nodes_types"]["names"]:
                tree_dict["nodes_types"]["names"].append("missing_go_to_left")
                tree_dict["nodes_types"]["formats"].append("uint8")
                tree_dict["nodes_types"]["offsets"].append(56)
                tree_dict["nodes_types"]["itemsize"] = 64

                updated_values = [(*t, 0) for t in tree_dict["nodes_values"]]
                tree_dict["nodes_values"] = updated_values
            else:
                updated_values = [(*t[:-1], 0) for t in tree_dict["nodes_values"]]
                tree_dict["nodes_values"] = updated_values

        del tree_dict["nodes"]

        return tree_dict

    @staticmethod
    def _get_structured_nparray_types(array: "np.ndarray") -> Dict[str, Any]:
        result = {"names": [], "formats": [], "offsets": [], "itemsize": array.dtype.itemsize}
        for field_name, field_info in array.dtype.fields.items():
            result["names"].append(field_name)
            result["formats"].append(field_info[0].__str__())
            result["offsets"].append(field_info[1])

        return result

    def create_numerical_attribute_binning_dmupto5_5_2(
        self,
        data: "pd.DataFrame",
        col_attribute: str,
        col_target: str,
        n_bins: int = 7,
        bins: Optional[List[Union[int, float]]] = None,
    ) -> Dict[str, Any]:
        """Create attribute binning for monitoring purposes. Bins are established to contain similar share of population
        (based on percentiles).

        :param: data: Data sample to be used for binning creation.
        :param: col_attribute: Attribute's name.
        :param: col_target: Name of the target.
        :param: n_bins: Number of bins to be created.
        :return: AttributeBinning object
        """

        # for numerical attributes, n same frequent bins are defined
        attribute_binning = {"dtype": "NUMERICAL"}

        import numpy as np

        if bins is None:
            if len(data[col_attribute].unique()) > n_bins:
                bins = list(
                    np.unique(
                        np.percentile(
                            data[data[col_attribute].notnull()][col_attribute], np.linspace(0, 100, n_bins + 1)
                        )
                    )
                )
                bins[0] = -np.inf
                bins[-1] = np.inf
            else:
                bins = sorted(data[col_attribute].unique().tolist())
                bins.insert(0, -np.inf)
                bins.append(np.inf)

        attribute_binning["bins"] = [-987654321.987654321] + bins[1:-1] + [987654321.987654321]

        frequency_null, target_rate_null = self._get_numerical_bin_frequency_and_target_rate(
            data=data, col_attribute=col_attribute, col_target=col_target, lower_bound=None, upper_bound=None
        )

        attribute_binning["null_frequency"] = frequency_null
        attribute_binning["null_target_rate"] = target_rate_null

        frequencies = []
        target_rates = []
        for i in range(len(bins) - 1):
            lower_bound = bins[i]
            upper_bound = bins[i + 1]

            frequency, target_rate = self._get_numerical_bin_frequency_and_target_rate(
                data=data,
                col_attribute=col_attribute,
                col_target=col_target,
                lower_bound=lower_bound,
                upper_bound=upper_bound,
            )

            frequencies.append(frequency)
            target_rates.append(target_rate)

        attribute_binning["bin_frequencies"] = frequencies
        attribute_binning["bin_target_rates"] = target_rates

        return attribute_binning

    def create_categorical_attribute_binning_dmupto5_5_2(
        self,
        data: "pd.DataFrame",
        col_attribute: str,
        col_target: str,
        n_bins: int = 7,
        categories: Optional[List[List[str]]] = None,
    ):
        # for numerical attributes, n same frequent bins are defined
        attribute_binning = {"dtype": "CATEGORICAL"}

        if categories is None:
            categories_raw = [
                cat for cat in data[col_attribute].value_counts(sort=True, ascending=False, dropna=True).index
            ]

            categories: List[List[str]] = []
            for i in range(min(n_bins - 1, len(categories_raw))):
                categories.append([categories_raw[i]])

            if len(categories_raw) >= n_bins:
                categories.append(categories_raw[n_bins:])

        attribute_binning["bins"] = categories

        frequency_null, target_rate_null = self._get_categorical_bin_frequency_and_target_rate(
            data=data, col_attribute=col_attribute, col_target=col_target, bin_categories=None
        )

        attribute_binning["null_target_rate"] = target_rate_null
        attribute_binning["null_frequency"] = frequency_null

        frequencies = []
        target_rates = []
        for i in range(len(categories)):
            frequency, target_rate = self._get_categorical_bin_frequency_and_target_rate(
                data=data, col_attribute=col_attribute, col_target=col_target, bin_categories=categories[i]
            )

            frequencies.append(frequency)
            target_rates.append(target_rate)

        attribute_binning["bin_frequencies"] = frequencies
        attribute_binning["bin_target_rates"] = target_rates

        return attribute_binning

    def get_monitoring_data_old(
        self, data: "pd.DataFrame", attributes: List[str], label_name: str, binning: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Dict[str, Any]]:
        if binning is None:
            binning = {}

        import pandas as pd

        monitoring_data = {}
        for attr in attributes:
            if attr not in data.columns:
                logger.warning(
                    f"Attribute {attr} was not found in provided dataset. Skipping preparation of monitoring "
                    f"data for this attribute."
                )
            if pd.api.types.is_numeric_dtype(data[attr].dtype):
                monitoring_data[attr] = self.create_numerical_attribute_binning_dmupto5_5_2(
                    data=data, col_attribute=attr, col_target=label_name, bins=binning.get(attr, {}).get("bins", None)
                )
            else:
                monitoring_data[attr] = self.create_categorical_attribute_binning_dmupto5_5_2(
                    data=data,
                    col_attribute=attr,
                    col_target=label_name,
                    categories=binning.get(attr, {}).get("categories", None),
                )
        return monitoring_data
