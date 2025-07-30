################################################################################
# weather_mcp/main.py
# This module provides a FastMCP wrapper for historical weather data.
################################################################################

import logging
import sys
from datetime import datetime, timedelta
from importlib import metadata

import pandas as pandas
from fastmcp import FastMCP
from meteostat import Daily, Hourly, Point, Stations, units

logger = logging.getLogger(__name__)

# Version handling
try:
    __version__ = metadata.version("weather-mcp")
except metadata.PackageNotFoundError:
    # Fallback to _version.py if package not installed
    try:
        from ._version import __version__
    except ImportError:
        __version__ = "unknown"

TIMESERIES_MAP = {"hourly": Hourly, "daily": Daily}

UNITS_MAP = {"imperial": units.imperial, "scientific": units.scientific}


def point_str(point):
    """
    Meteostat lacks public accessors, so instead of suppressing static analysis
    warnings in multiple places, it is done once here.
    This could break on newer versions of the module.
    :param point: A Meteostat point.
    :return: A formatted string.
    """
    # noinspection PyProtectedMember
    return f"({point._lat:.4f}, {point._lon:.4f})"


# def get_nearby_weather_stations(
#     lat: float, lon: float, search_radius_km: int = 150, max_stations: int = 25
# ) -> pandas.DataFrame:
#     """
#     Get nearby weather stations, ordered by distance (nearest to furthest).
#
#     Args:
#         lat: latitude of the point (-90 to 90)
#         lon: longitude of the point (-180 to 180)
#         search_radius_km: the station search radius in km
#         max_stations: the maximum number of stations to return
#     """
#     search_radius_m = search_radius_km * 1000
#     stations: pandas.DataFrame = (
#         Stations()
#         .nearby(lat=lat, lon=lon, radius=search_radius_m)
#         .fetch(max_stations)
#     )
#     logger.info(f"Found {stations.shape[0]} stations within {search_radius_km}km.")
#     return stations


def find_nearest_station_with_best_coverage(
    lat: float,
    lon: float,
    search_radius_km: int | None = None,
    max_stations: int = 25,
    date: str | None = None,
    timeseries_type: str | None = None,
    coverage_threshold: float | None = None,
    measurement_units: str | None = None,
):
    """
    Examine a list of weather stations to find the nearest station with good data
    coverage.

    Args:
        # stations: a Pandas DataFrame containing a list of weather stations.
        lat: latitude of the point (-90 to 90)
        lon: longitude of the point (-180 to 180)
        search_radius_km: the station search radius in km
        max_stations: the maximum number of stations to return
        date: the date to search for coverage in YYYY-MM-DD format
            (will default to yesterday's date).
        timeseries_type: Use hourly for temperature, pressure, wind, and weather
            conditions; daily for precipitation, snow, and sun totals.
        coverage_threshold: the percent data coverage (0.0 to 1.0) that will stop
            the station search from expanding further.
        measurement_units: the units the measurements should be returned in
            (imperial or scientific).
    """
    # Set defaults for None parameters
    if search_radius_km is None:
        search_radius_km = 150
    if timeseries_type is None:
        timeseries_type = "hourly"
    if coverage_threshold is None:
        coverage_threshold = 0.50
    if measurement_units is None:
        measurement_units = "imperial"
    if date is None:
        date = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    if timeseries_type not in TIMESERIES_MAP:
        raise KeyError(
            f"Invalid timeseries_type '{timeseries_type}'. "
            f"Must be one of {list(TIMESERIES_MAP.keys())}"
        )

    if measurement_units not in UNITS_MAP:
        raise KeyError(
            f"Invalid measurement_units '{measurement_units}'. "
            f"Must be one of {list(UNITS_MAP.keys())}"
        )

    search_radius_m = search_radius_km * 1000
    stations: pandas.DataFrame = (
        Stations().nearby(lat=lat, lon=lon, radius=search_radius_m).fetch(max_stations)
    )
    logger.info(f"Found {stations.shape[0]} stations within {search_radius_km}km.")

    s_time: datetime = datetime.strptime(date, "%Y-%m-%d")
    e_time: datetime = s_time.replace(hour=23, minute=59)
    timeseries_class = TIMESERIES_MAP[timeseries_type]
    units_class = UNITS_MAP[measurement_units]

    api_query = None
    best_coverage: float = 0.0
    station = None

    for index, station_row in stations.iterrows():
        station_df = stations.loc[[index]]
        timeseries_query = timeseries_class(loc=station_df, start=s_time, end=e_time)

        # noinspection PyArgumentList
        coverage: float = (
            timeseries_query.coverage()
        )  # check the station coverage for this date

        if coverage > best_coverage:
            logger.debug(
                f"Found{' better' if station is not None else ''} station: "
                f"{index} with {coverage:.2%} coverage."
            )
            api_query = timeseries_query
            station = station_row
            best_coverage = coverage
            if coverage >= coverage_threshold:
                break  # stop looking if the coverage is sufficient

    if api_query is None:
        raise ValueError(
            f"No stations in list have coverage for {s_time.strftime('%Y-%m-%d')}."
        )

    # noinspection PyArgumentList
    api_query.convert(units_class)

    if logger.isEnabledFor(logging.DEBUG):
        pandas.set_option("display.max_rows", None)
        pandas.set_option("display.max_columns", None)

    logger.debug(station)

    return api_query, station


def get_weather(
    lat: float,
    lon: float,
    date: str | None = None,
    search_radius_km: int = 150,
    timeseries_type: str = "hourly",
    coverage_threshold: float = 0.50,
    measurement_units: str = "imperial",
) -> dict | None:
    """
    Get hourly or daily weather data for a given latitude and longitude
    on a specific date using meteostat.

    Args:
        lat: latitude of the point (-90 to 90)
        lon: longitude of the point (-180 to 180)
        date: date in YYYY-MM-DD format (will default to yesterday's date).
        search_radius_km: the station search radius in km
        timeseries_type: Use hourly for temperature, pressure, wind, and weather
            conditions; daily for precipitation, snow, and sun totals.
        coverage_threshold: the percent data coverage (0.0 to 1.0) that will stop
            the station search from expanding further.
        measurement_units: the units the measurements should be returned in
            (imperial or scientific).

    Returns:
        dict: Weather data, station metadata, and coverage or None if no data
            could be retrieved.
    """
    point = Point(lat, lon)

    try:
        # noinspection PyProtectedMember
        # s: pandas.DataFrame = get_nearby_weather_stations(
        #     lat=point._lat, lon=point._lon, search_radius_km=search_radius_km
        # )
        # api_query = find_nearest_station_with_best_coverage(
        #     s, date, timeseries_type, coverage_threshold, measurement_units
        # )

        api_query, station = find_nearest_station_with_best_coverage(
            lat=point._lat,
            lon=point._lon,
            search_radius_km=search_radius_km,
            date=date,
            timeseries_type=timeseries_type,
            coverage_threshold=coverage_threshold,
            measurement_units=measurement_units,
        )

        # noinspection PyArgumentList
        coverage: float = api_query.coverage()
        # noinspection PyArgumentList
        weather_df: pandas.DataFrame = api_query.fetch()

        logger.debug(weather_df)

        return {
            "data": weather_df.to_dict(),
            "station": station.to_dict(),
            "coverage": coverage,
        }
    except KeyError:
        raise
    except Exception as e:
        import traceback

        logger.warning(f"Error processing location {point_str(point)}, {date}: {e}")
        logger.debug(traceback.format_exc())
        return None  # TODO: Should this raise the exception instead?


# MAIN SECTION
# Create the FastMCP instance
mcp: FastMCP = FastMCP("weather_mcp")

# Register all tools
# mcp.tool(point_str)
# mcp.tool(get_nearby_weather_stations)
# mcp.tool(find_nearest_station_with_best_coverage)
mcp.tool(get_weather)


def main():
    """Main entry point for the application."""
    if "--version" in sys.argv:
        print(__version__)
        sys.exit(0)
    mcp.run()


if __name__ == "__main__":
    main()
