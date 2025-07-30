import requests
import pandas as pd
from typing import Dict, Optional, Union, Mapping

def forecastfactor_publish(
    api_key: str,
    group_name: str,
    series_name: str,
    model_name: str,
    transformation_name: str,
    data_frequency: str,
    raw_data: pd.DataFrame,
    forecast_data: pd.DataFrame,
    forecast_bounds: pd.DataFrame,
    forecast_residuals: pd.DataFrame,
    turning_points: Dict[str, list],
    metadata: Mapping[str, Union[str, int, float]],
    model_inputs: Mapping[str, Union[str, int, float]],
    model_info: Dict[str, list],
    base_url: Optional[str] = None,
    environment: str = "prod",
):
    """
    Posts time series data, metadata to an API.
 
    Parameters:
        api_key (str): API key for authentication.
        group_name (str): The name of the group the series belongs to.
        series_name (str): The name of the series.
        model_name (str): The name of the model.
        transformation_name (str): The name of the transformation of the original dataset to feed the model (e.g., 'none', 'log', etc.).
        data_frequency (str): The series data frequency (monthly, weekly, daily, etc.).
        raw_data (pd.DataFrame): DataFrame of raw time series data with columns ['date', 'value'].
        forecast_data (pd.DataFrame): DataFrame of forecast bounds with columns ['date', 'value'].
        forecast_bounds (pd.DataFrame): DataFrame of forecast data with columns ['date', 'lb95', ..., 'up95'].
        forecast_residuals (pd.DataFrame): DataFrame of forecast data with columns ['date', 'value'].
        turning_points (Dict): Dictionary where keys are timestamps, and values are lists of turning points.
        metadata (Dict): Additional metadata characterizing the series and input parameters. Values can be str, int, or float.
        model_inputs (Dict): Information about the forecasting model, including performance metrics. Values can be str, int, or float.
        model_info (Dict): Dictionary where keys are model parameters, and values are lists of multiple values.
        base_url (str, optional): Override the default API endpoint URL. Defaults to None (uses the official endpoint).
        environment (str, optional): Choose between 'dev' and 'prod' environments. Defaults to 'prod'.
 
    Returns:
        Dict: Response from the API.
    """
    # Validate turning_points format
    if not isinstance(turning_points, dict) or not all(isinstance(v, list) for v in turning_points.values()):
        return {"status": "error", "message": "Invalid format: 'turningPoints' should be a dictionary with lists as values."}

    # Validate model_info format
    if not isinstance(model_info, dict) or not all(isinstance(v, list) for v in model_info.values()):
        return {"status": "error", "message": "Invalid format: 'modelInfo' should be a dictionary with lists as values."}

    # Validate environment parameter
    if environment not in ["dev", "prod"]:
        return {"status": "error", "message": "Invalid environment. Must be 'dev' or 'prod'."}

    payload = {
        "groupName": group_name,
        "seriesName": series_name,
        "modelName": model_name,
        "transformationName": transformation_name,
        "dataFrequency": data_frequency,
        "rawData": raw_data.to_dict(orient="records"),
        "forecastData": forecast_data.to_dict(orient="records"),
        "forecastBounds": forecast_bounds.to_dict(orient="records"),
        "forecastResiduals": forecast_residuals.to_dict(orient="records"),
        "turningPoints": turning_points,
        "metadata": metadata,
        "modelInfo": model_info,
        "modelInputs": model_inputs,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        if base_url:
            url = base_url
        else:
            base_endpoint = "https://forecastfactor-ingestor.ricardofmteixeira.workers.dev/"
            if environment == "dev":
                url = base_endpoint.replace("forecastfactor-ingestor", "dev-forecastfactor-ingestor")
            else:
                url = base_endpoint
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)
        return {"status": "success", "message": "Forecast data successfully uploaded."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request failed: {str(e)}"}