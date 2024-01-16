import pandas as pd


def read_assets():
    """
    Read assets from the CSV file and return a list of asset records.

    \f
    Returns:
        List[dict]: A list of asset records with fields 'asset_id' and 'name'.

        asset_id: Asset ID from the .CSV file.
        name: Asset name from the .CSV file.
    """

    df = pd.read_csv("app/assets/assets.csv")
    assets = df.to_dict(orient="records")
    return assets


def read_measurements():
    """
    Read measurements from the CSV file, filter rows with null values,
    and return a list of formatted measurement records.

    \f
    Returns:
        List[dict]: A list of measurement records with fields 'asset_id', 'timestamp',
        'wind_speed', 'power', and 'air_temperature'.

        asset_id: Asset ID from the .CSV file.
        timestamp: Date and time when the measurement was taken.
        wind_speed: Wind speed at the time of the measurement.
        power: Power at the time of the measurement.
        air_temperature: Air temperature at the time of the measurement.
    """

    df = pd.read_csv("app/measurements/measurements.csv")
    df.dropna(inplace=True)
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S.%f %z")
    measurements = df.to_dict(orient="records")
    return measurements


def create_average(request):
    """
    Calculate the average value of a specific column (wind_speed, power, or air_temperature)
    for a selected set of assets and a specific time period.

    \f
    Args:
        request (AverageRequest): An AverageRequest object containing information about the assets,
        column, start date, and end date.

    Returns:
        Union[AverageResponse, Dict[str, str]]: The response object containing asset names and the average value of the column
        if successful. If there's an error, a dictionary with an error message is returned.

        asset_names: A list of asset names from the .CSV file.
        average_value: Calculated value using the chosen row, within the chosen time and the chosen asset_ids.
    """

    df_assets = pd.read_csv("app/assets/assets.csv")
    df = pd.read_csv("app/measurements/measurements.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"], format="%Y-%m-%d %H:%M:%S.%f %z")

    valid_asset_ids = df["asset_id"].unique()
    for asset_id in request.asset_ids:
        if asset_id not in valid_asset_ids:
            return {"error": f"Asset with ID {asset_id} does not exist in the data."}

    filtered_df = df[(df["asset_id"].isin(request.asset_ids))]
    if request.column not in filtered_df.columns:
        return {"error": f"Column '{request.column}' not found in the data."}
    elif request.end_date < request.start_date:
        return {"error": "End date is before the start date."}
    elif request.end_date == request.start_date:
        return {"error": "Start date cannot be the same as the end date."}
    elif (
        request.start_date > filtered_df["timestamp"].max()
        or request.end_date < filtered_df["timestamp"].min()
    ):
        return {"error": "Dates do not exist in the data."}
    elif request.start_date < filtered_df["timestamp"].min():
        request.start_date = filtered_df["timestamp"].min()
    if request.end_date > filtered_df["timestamp"].max():
        request.end_date = filtered_df["timestamp"].max()

    filtered_df = filtered_df[
        (filtered_df["timestamp"] >= request.start_date)
        & (filtered_df["timestamp"] <= request.end_date)
    ]

    average_value = filtered_df[request.column].mean()
    asset_ids = [int(asset_id) for asset_id in request.asset_ids]
    asset_names = df_assets[df_assets["asset_id"].isin(asset_ids)]["name"].tolist()

    average_data = {"asset_names": asset_names, "average_value": average_value}
    return average_data
