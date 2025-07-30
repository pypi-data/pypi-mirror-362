# Python SDK

Advisor Software Development Kit for python.

## Contents
- [Python SDK](#python-sdk)
  - [How to get your token](https://www.climatempoconsultoria.com.br/contato/)
  - [Contents](#contents)
  - [Importing](#importing)
  - [Routes](#routes)
    - [Examples](#examples)
      - [Chart](#chart)
      - [Climatology](#climatology)
      - [Current Weather](#current-weather)
      - [Forecast](#forecast)
      - [Monitoring](#monitoring)
      - [Observed](#observed)
      - [Plan Information](#plan-information)
      - [Static Map](#static-map)
      - [Storage](#storage)
      - [Schema/Parameter](#schemaparameter)
      - [Tms (Tiles Map Server)](#tms-tiles-map-server)
  - [Headers Configuration](#headers-configuration)
  - [Response Format](#response-format)
  - [Payload Types](#payload-types)
    - [WeatherPayload](#weatherpayload)
    - [StationPayload](#stationpayload)
    - [ClimatologyPayload](#climatologypayload)
    - [CurrentWeatherPayload](#currentweatherpayload)
    - [RadiusPayload](#radiuspayload)
    - [GeometryPayload](#geometrypayload)
    - [TmsPayload](#tmspayload)
    - [RequestDetailsPayload](#requestdetailspayload)
---
## Importing

To install this package, use the following command:`

```bash
pip install stormgeo.advisor-core
```

Make sure you're using python 3.8 or higher.


## Routes

First you need to import the SDK on your application and instancy the `AdvisorCore` class setting up your access token and needed configurations:

```python
from advisor_core import *

advisor = AdvisorCore("<your_token>", retries=5, delay=5)
```

### Examples
Get data from different routes with theses examples

#### Chart
```python
payload = WeatherPayload(
  locale_id=1234,
  variables=["temperature", "precipitation"]
)

# requesting daily forecast chart image
response = advisor.chart.get_forecast_daily(payload)

# requesting hourly forecast chart image
response = advisor.chart.get_forecast_hourly(payload)

# requesting daily observed chart image
response = advisor.chart.get_observed_daily(payload)

# requesting hourly observed chart image
response = advisor.chart.get_observed_hourly(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  with open("response.png", "wb") as f:
    f.write(response["data"])
```

#### Climatology
```python
payload = ClimatologyPayload(
  locale_id=1234,
  variables=["temperature", "precipitation"]
)

# requesting daily climatology data
response = advisor.climatology.get_daily(payload)

# requesting monthly climatology data
response = advisor.climatology.get_monthly(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Current Weather
```python
payload = CurrentWeatherPayload(
  locale_id=1234
)

response = advisor.current_weather.get(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```


#### Forecast
```python
payload = WeatherPayload(
  locale_id=1234,
  variables=["temperature", "precipitation"]
)

# requesting daily forecast data
response = advisor.forecast.get_daily(payload)

# requesting hourly forecast data
response = advisor.forecast.get_hourly(payload)

# requesting period forecast data
response = advisor.forecast.get_period(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Monitoring
```python
response = advisor.monitoring.get_alerts()

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Observed
```python
payload = WeatherPayload(
  locale_id=1234,
)

payload_for_station = StationPayload(
  station_id="ABC123abc321CBA"
)

payload_for_radius = RadiusPayload(
  locale_id=1234,
  radius=1000
)

payload_for_geometry = GeometryPayload(
  geometry="{\"type\": \"MultiPoint\", \"coordinates\": [[-41.88, -22.74]]}",
  radius=10000
)

# requesting daily observed data
response = advisor.observed.get_daily(payload)

# requesting hourly observed data
response = advisor.observed.get_hourly(payload)

# requesting period observed data
response = advisor.observed.get_period(payload)

# requesting station observed data
response = advisor.observed.get_station_data(payload_for_station)

# requesting fire-focus observed data
response = advisor.observed.get_fire_focus(payload_for_radius)

# requesting lightning observed data
response = advisor.observed.get_lightning(payload_for_radius)

# requesting fire-focus observed data by geometry
response = advisor.observed.get_fire_focus_by_geometry(payload_for_geometry)

# requesting lightning observed data by geometry
response = advisor.observed.get_lightning_by_geometry(payload_for_geometry)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Storage
```python
payload = StorageListPayload(
  page=1,
  page_size=10
)

payload_for_download = StorageDownloadPayload(
  file_name="Example.pdf",
  access_key="a1b2c3d4-0010"
)

# requesting the files list
response = advisor.storage.list_files(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])

# downloading a file from the list
response = advisor.storage.download_file(payload_for_download)

if response['error']:
    print('Error trying to get data')
    print(response['error'])
else:
    with open(payload_for_download.file_name, "wb") as f:
        f.write(response["data"])

# downloading a file by stream
response = advisor.storage.download_file_by_stream(payload_for_download)

if response['error']:
    print('Error trying to get data')
    print(response['error'])
else:
    with open(payload_for_download.file_name, "wb") as f:
        for chunk in response['data']:
            if chunk:
                f.write(chunk)
```

#### Plan Information
```python
payload = PlanInfoPayload(
  timezone=-3
)

payload_for_details = RequestDetailsPayload(
  page=1,
  page_size=10
)

# requesting plan information
response = advisor.plan.get_info(payload)

# requesting access history
response = advisor.plan.get_request_details(payload_for_details)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Static Map
```python
payload = StaticMapPayload(
    type="periods",
    category="observed",
    variable="temperature",
    aggregation="max",
    start_date="2025-07-01 00:00:00",
    end_date="2025-07-05 23:59:59",
    dpi=50,
    title=True,
    titlevariable="Static Map",
)

response = advisor.static_map.get_static_map(payload)

if response['error']:
    print('Error trying to get data!')
    print(response['error'])
else:
    with open("response.png", "wb") as f:
        f.write(response["data"])
```

#### Schema/Parameter
```python
# Arbitrary example on how to define a schema
payload_schema_definition = {
  "identifier": "arbitraryIdentifier",
  "arbitraryField1": {
      "type": "boolean",
      "required": True,
      "length": 125,
  },
  "arbitraryField2": {
      "type": "number",
      "required": True,
  },
  "arbitraryField3": {
      "type": "string",
      "required": False,
  }
}

# Arbitrary example on how to upload data to parameters from schema 
payload_schema_parameters = {
  "identifier": "arbitraryIdentifier",
  "arbitraryField1": True,
  "arbitraryField2": 15
}

# requesting all schemas from token
response = advisor.schema.get_definition()

# requesting to upload a new schema
response = advisor.schema.post_definition(payload_schema_definition)

# requesting to upload data to parameters from schema
response = advisor.schema.post_parameters(payload_schema_parameters)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  print(response['data'])
```

#### Tms (Tiles Map Server)
```python
payload = TmsPayload(
  istep="2024-12-25 10:00:00",
  fstep="2024-12-25 12:00:00",
  server="a",
  mode="forecast",
  variable="precipitation",
  aggregation="sum",
  x=2,
  y=3,
  z=4
)

response = advisor.tms.get(payload)

if response['error']:
  print('Error trying to get data!')
  print(response['error'])
else:
  with open("response.png", "wb") as f:
    f.write(response["data"])
```

---

## Headers Configuration

You can also set headers to translate the error descriptions or to receive the response in a different format type. This functionality is only available for some routes, consult the API documentation to find out which routes have this functionality.

Available languages: 
- en-US (default)
- pt-BR
- es-ES

Available response types:
- application/json (default)
- application/xml
- text/csv

Example:

```javascript
advisor = AdvisorCore("invalid-token")

advisor.setHeaderAccept("application/xml")
advisor.setHeaderAcceptLanguage("es-ES")

response = advisor.plan.get_info()

print(response["error"])

// <response>
//   <error>
//     <type>UNAUTHORIZED_ACCESS</type>
//     <message>UNAUTHORIZED_REQUEST</message>
//     <description>La solicitud no está autorizada.</description>
//   </error>
// </response>
```

## Response Format

All the methods will return the same pattern:

```python
{
  "data": Any | None,
  "error": Any | None,
}
```

## Payload Types

### WeatherPayload

- **locale_id**: int
- **station_id**: str
- **latitude**: float
- **longitude**: float
- **timezone**: int
- **variables**: List[str]
- **start_date**: str
- **end_date**: str

### StationPayload

- **station_id**: str
- **layer**: str
- **variables**: List[str]
- **start_date**: str
- **end_date**: str

### ClimatologyPayload

- **locale_id**: int
- **station_id**: str
- **latitude**: float
- **longitude**: float
- **variables**: List[str]

### CurrentWeatherPayload

- **locale_id**: int
- **station_id**: str
- **latitude**: float
- **longitude**: float
- **timezone**: int
- **variables**: List[str]

### RadiusPayload

- **locale_id**: int
- **station_id**: str
- **latitude**: float
- **longitude**: float
- **start_date**: str
- **end_date**: str
- **radius**: int

### GeometryPayload

- **start_date**: str
- **end_date**: str
- **radius**: int
- **geometry**: str

### TmsPayload

- **server**: str
- **mode**: str
- **variable**: str
- **aggregation**: str
- **x**: int
- **y**: int
- **z**: int
- **istep**: str
- **fstep**: str
- **timezone**: int

### PlanInfoPayload
- **timezone**: int

### RequestDetailsPayload

- **page**: int
- **page_size**: int
- **path**: str
- **status**: int
- **start_date**: str
- **end_date**: str

### StorageListPayload

- **page**: int
- **page_size**: int
- **start_date**: str
- **end_date**: str
- **file_name**: str
- **file_extension**: str

### StorageDownloadPayload

- **file_name**: str
- **access_key**: str

### StaticMapPayload

- **start_date**: str  
- **end_date**: str  
- **aggregation**: str  
- **model**: str  
- **lonmin**: float  
- **latmin**: float  
- **lonmax**: float  
- **latmax**: float  
- **dpi**: int  
- **title**: bool  
- **titlevariable**: str  
- **hours**: int  
- **type**: str
- **category**: str
- **variable**: str

---