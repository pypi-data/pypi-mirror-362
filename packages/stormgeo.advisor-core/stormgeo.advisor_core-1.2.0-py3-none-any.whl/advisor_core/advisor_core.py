from .request_handler import RequestHandler
from .header import Header
from .grouped_routes import (
    ForecastAPI,
    ObservedAPI,
    CurrentWeatherAPI,
    ClimatologyAPI,
    MonitoringAlertsAPI,
    PlanAPI,
    ChartAPI,
    TmsAPI,
    SchemaAPI,
    StorageAPI,
    StaticMapAPI,
)

class AdvisorCore:
    """
    Central class that encapsulates access to various routes of the Advisor API.
    """
    def __init__(self, token, retries=5, delay=5):
        base_url="https://advisor-core.climatempo.io/api/"
        self._header = Header()
        self._header.set('Accept', 'application/json')
        self._header.set('Content-Type', 'application/json')
        self._header.set('x-advisor-token', token)
        request_handler = RequestHandler(base_url, token, retries, delay, self._header)
        self.forecast = ForecastAPI(request_handler) 
        """Fetch weather forecast."""
        self.observed = ObservedAPI(request_handler)
        """Fetch observed weather."""
        self.current_weather = CurrentWeatherAPI(request_handler)
        """Fetch current weather."""
        self.climatology = ClimatologyAPI(request_handler)
        """Fetch climatology weather."""
        self.monitoring = MonitoringAlertsAPI(request_handler)
        """Fetch alerts."""
        self.storage = StorageAPI(request_handler)
        """Fetch bucket files."""
        self.plan = PlanAPI(request_handler)
        """Fetch plan information."""
        self.chart = ChartAPI(request_handler)
        """Fetch weather data charts"""
        self.static_map = StaticMapAPI(request_handler)
        """Fetch static map images."""
        self.tms = TmsAPI(request_handler)
        """Fetch tiles map service."""
        self.schema = SchemaAPI(request_handler)
        """Get and set schema/parameters."""

    def setHeaderAccept(self, value):
        self._header.set('Accept', value)

    def setHeaderToken(self, value):
        self._header.set('x-advisor-token', value)
    
    def setHeaderAcceptLanguage(self, value):
        self._header.set('Accept-Language', value)
