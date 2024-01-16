from fastapi import FastAPI
from typing import Union, Dict
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.api.data_api import read_assets, read_measurements, create_average

app = FastAPI()


class Asset(BaseModel):
    """
    Represents an asset with its ID and name.

    \f
    Attributes:
        asset_id (int): Asset ID from the CSV file.
        name (str): The name of the asset.
    """

    asset_id: int
    name: str


class Measurement(BaseModel):
    """
    Represents a measurement data point.

    \f
    Attributes:
        asset_id (int): Asset ID associated with the measurement.
        timestamp (datetime): Date and time when the measurement was taken.
        wind_speed (float): Wind speed at the time of the measurement.
        power (float): Power at the time of the measurement.
        air_temperature (float): Air temperature at the time of the measurement.
    """

    asset_id: int
    timestamp: datetime
    wind_speed: float
    power: float
    air_temperature: float


class AverageRequest(BaseModel):
    """
    Represents a request for calculating the average value.

    \f
    Attributes:
        asset_ids (List[int]): List of asset IDs to calculate the average for.
        column (str): The column for which the average is calculated (e.g., 'wind_speed', 'power', 'air_temperature').
        start_date (datetime): The start date for the time period of interest.
        end_date (datetime): The end date for the time period of interest.
    """

    asset_ids: List[int]
    column: str
    start_date: datetime
    end_date: datetime


class AverageResponse(BaseModel):
    """
    Represents the response for calculating the average value.

    \f
    Attributes:
        asset_names (List[str]): List of asset names corresponding to the provided asset IDs.
        average_value (float): The calculated average value.
    """

    asset_names: List[str]
    average_value: float


@app.get("/assets", response_model=List[Asset])
def list_assets():
    """
    Endpoint to list all available assets.

    \f
    Returns:
        List[Asset]: A list of Asset objects representing available assets.
    """

    assets = read_assets()
    return assets


@app.get("/measurements", response_model=List[Measurement])
def list_measurements():
    """
    Endpoint to list all available measurements.

    \f
    Returns:
        List[Measurement]: A list of Measurement objects representing available measurements.
    """

    measurements = read_measurements()
    return measurements


@app.post("/average_value")
def calculate_average_value(
    request: AverageRequest,
) -> Union[AverageResponse, Dict[str, str]]:
    """
    Endpoint to calculate the average value of a specific column for selected assets within a time period.

    \f
    Args:
        request (AverageRequest): The request object containing parameters for calculation.

    Returns:
        Union[AverageResponse, Dict[str, str]]: The response object containing asset names and the calculated average value
        if successful. If there's an error, a dictionary with an error message is returned.

    """

    average_data = create_average(request)
    return average_data
