# TaranDM analytics

TaranDM analytics is a package with supportive functions for TaranDM decision manager software. Two main areas are covered:
- Preparation of predictive model deployment
- Preparation of dataset for predictive model development - attribute evaluator

An **example notebook** how to use `tarandm_analytics` is included in the package in `tarandm_analytics/examples/tarandm_model_development.ipynb` 

## Predictive model deployment
Strategies in TaranDM can contain predictive models. For compatibility, TaranDM requires specific format in which the 
model is deployed. `tarandm_analytics` package provides functions to make the deployment easy.

In TaranDM, predictive models are stored alongside with additional metadata. Those can be used for instance to monitor 
the model stability. Information about development sample and model performance is also stored amongst others.

After training the predictive model, steps to prepare the model for deployment would typically be:
1. Initialize `ExportPredictiveModel` from `tarandm_analytics` package.
2. Prepare monitoring data using `get_monitoring_data` method. This will calculate data to monitor stability through 
population stability index (PSI).
3. Prepare predictive model data for export to disk using `prepare_predictive_model_data` method.
4. Export model to disk using `build_predictive_model` method. Model is exported in zip format, that can be uploaded to 
TaranDM strategy in GUI.

## Attribute evaluator

Attribute evaluator provides functions to create a dataset for predictive model development. Past requests are fetched 
from database and attributes defined in TaranDM attribute classes are evaluated. It uses the same code to evaluate 
attributes as the production environment, which eliminates potential mismatch in attribute definition during 
implementation to production.

User can either define past requests to be included in the dataset by listing decision ids directly or by defining 
business case and time range. Attribute classes to be evaluated are also defined by user.

To prepare the dataset:
1. Initialize `EvaluateAttributes` class.
2. List available attribute classes using `get_attribute_classes`.
3. List available business cases using `get_business_cases`.
4. Run `evaluate` method. Business case, time range or list of decision ids are provided as parameters of the method. 
Note that user is required to provide Git repository with strategies as well as credentials for the repository.
5. Once the attributes are evaluated, fetch the data using `fetch_data_from_db` method. It requires process ID as a 
parameter. This can be found in `last_attribute_extractor_id` property of `EvaluateAttributes` object.

