# FASTAPI-TEST

This API, developed using FastAPI, allows you to analyze asset data efficiently. It offers the following features:

List all available assets.
Retrieve a list of all measurements.
Calculate the average value of specific columns (wind_speed, power, or air_temperature) for selected assets within a specified time range.

# GETTING STARTED


## Installation

Clone this repository and use the commands:

```bash
   git clone https://github.com/jpmouradev/fastapi-test.git
   cd fastapi-test
   docker-compose up --build
```
    
## Usage

#### Get all assets

```http
  GET /assets
```

#### Get all measurements

```http
  GET /measurements
```


#### Get an average value

```http
  POST /average_value

  Example Request Body:

{
  "asset_ids": [101, 102],
  "column": "power",
  "start_date": "2035-08-11T00:00:00Z",
  "end_date": "2035-08-15T00:00:00Z"
}
```


## Response (Average value)

#### Example Response

```http
  Example Request Body:

{
  "asset_names": ["WTG 01", "WTG 02"],
  "average_value": 123.45
}
```

#### Example Error

```http
  Example Error Body:

{
  "error": "End date is before the start date."
}
```
