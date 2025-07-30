from typing import List

class WeatherPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        timezone: int = None,
        variables: List[str] = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Initializes the WeatherPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.variables = variables
        self.start_date = start_date
        self.end_date = end_date

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "variables[]": self.variables,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

class CurrentWeatherPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        timezone: int = None,
        variables: List[str] = None,
    ):
        """
        Initializes the CurrentWeatherPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.variables = variables
    
    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timezone": self.timezone,
            "variables[]": self.variables,
        }

class ClimatologyPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        variables: List[str] = None,
    ):
        """
        Initializes the ClimatologyPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id
        self.latitude = latitude
        self.longitude = longitude
        self.variables = variables

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "variables[]": self.variables,
        }

class RadiusPayload:
    def __init__(
        self,
        locale_id: int = None,
        station_id: str = None,
        latitude: float = None,
        longitude: float = None,
        start_date: str = None,
        end_date: str = None,
        radius: int = None,
    ):
        """
        Initializes the RadiusPayload object with optional parameters.
        """
        self.locale_id = locale_id
        self.station_id = station_id 
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.radius = radius

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "localeId": self.locale_id,
            "stationId": self.station_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "radius": self.radius,
        }

class StationPayload:
    def __init__(
        self,
        station_id: str = None,
        layer: str = None,
        variables: List[str] = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Initializes the StationPayload object with optional parameters.
        """
        self.station_id = station_id 
        self.layer = layer
        self.variables = variables
        self.start_date = start_date
        self.end_date = end_date

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "stationId": self.station_id,
            "layer": self.layer,
            "variables[]": self.variables,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

class GeometryPayload:
    def __init__(
        self,
        radius: int = None,
        start_date: str = None,
        end_date: str = None,
        geometry: str = None
    ):
        """
        Initializes the GeometryPayload object with optional parameters.
        """
        self.radius = radius
        self.start_date = start_date
        self.end_date = end_date
        self.geometry = geometry

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "radius": self.radius,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

    def getBody(self) -> dict:
        """
        Returns the body of the request with the geometry information.
        """
        return {
            "geometry": self.geometry,
        }

class TmsPayload:
    def __init__(
        self,
        istep: str = None,
        fstep: str = None,
        timezone: int = None,
        server: str = None,
        mode: str = None,
        variable: str = None,
        aggregation: str = None,
        x: int = None,
        y: int = None,
        z: int = None,
    ):
        """
        Initializes the TmsPayload object with optional parameters.
        """
        self.istep = istep
        self.fstep = fstep
        self.timezone = timezone
        self.server = server
        self.mode = mode
        self.variable = variable
        self.aggregation = aggregation
        self.x = x
        self.y = y
        self.z = z

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "istep": self.istep,
            "fstep": self.fstep,
            "timezone": self.timezone,
        }

class PlanInfoPayload:
    def __init__(
        self,
        timezone: int = None,
    ):
        """
        Initializes the PlanInfoPayload object with optional parameters.
        """
        self.timezone = timezone

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "timezone": self.timezone,
        }

class RequestDetailsPayload:
    def __init__(
        self,
        page: int = None,
        page_size: int = None,
        path: str = None,
        status: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Initializes the RequestDetailsPayload with optional parameters.
        """
        self.page = page
        self.page_size = page_size
        self.path = path
        self.status = status
        self.start_date = start_date
        self.end_date = end_date

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "page": self.page,
            "pageSize": self.page_size,
            "path": self.path,
            "status": self.status,
            "startDate": self.start_date,
            "endDate": self.end_date,
        }

class StorageListPayload:
    def __init__(
        self,
        page: int = None,
        page_size: int = None,
        start_date: str = None,
        end_date: str = None,
        file_name: str = None,
        file_extension: str = None,
    ):
        """
        Initializes the StorageListPayload with optional parameters.
        """
        self.page = page
        self.page_size = page_size
        self.start_date = start_date
        self.end_date = end_date
        self.file_name = file_name
        self.file_extension = file_extension

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "page": self.page,
            "pageSize": self.page_size,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "fileName": self.file_name,
            "fileExtension": self.file_extension,
        }

class StorageDownloadPayload:
    def __init__(
        self,
        file_name: str = None,
        access_key: str = None,
    ):
        """
        Initializes the StorageDownloadPayload with optional parameters.
        """
        self.file_name = file_name
        self.access_key = access_key

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "fileName": self.file_name,
            "accessKey": self.access_key,
        }

class StaticMapPayload:
    def __init__(
        self,
        start_date: str = None,
        end_date: str = None,
        aggregation: str = None,
        model: str = None,
        lonmin: float = None,
        latmin: float = None,
        lonmax: float = None,
        latmax: float = None,
        dpi: int = None,
        title: bool = None,
        titlevariable: str = None,
        hours: int = None,
        type: str = None,
        category: str = None,
        variable: str = None,
    ):
        """
        Initializes the StaticMapPayload object with optional parameters.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.aggregation = aggregation
        self.model = model
        self.lonmin = lonmin
        self.latmin = latmin
        self.lonmax = lonmax
        self.latmax = latmax
        self.dpi = dpi
        self.title = title
        self.titlevariable = titlevariable
        self.hours = hours
        self.type = type
        self.category = category
        self.variable = variable

    def get_params(self) -> dict:
        """
        Returns the parameters as a dictionary for API requests.
        """
        return {
            "startDate": self.start_date,
            "endDate": self.end_date,
            "aggregation": self.aggregation,
            "model": self.model,
            "lonmin": self.lonmin,
            "latmin": self.latmin,
            "lonmax": self.lonmax,
            "latmax": self.latmax,
            "dpi": self.dpi,
            "title": self.title,
            "titlevariable": self.titlevariable,
            "hours": self.hours,
        }
