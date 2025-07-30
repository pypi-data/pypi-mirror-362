import logging

import pytest
from meteostat import Point

from weather_mcp.main import get_weather

logger = logging.getLogger("weather_mcp.main")

date_hurricane_huron = "2013-08-27"
date_hurricane_katrina = "2005-08-29"
date_midsummer = "2025-06-19"

loc_baystlouis_ms = Point(30.3081058, -89.3308496)
loc_lansing_mi = Point(42.732536, -84.555534)
loc_port_austin_mi = Point(44.050166466, -82.900496398)
loc_port_huron_mi = Point(43.0056, -82.4187)
loc_detroit_mi = Point(42.3277305, -83.0505869)
loc_goderich_on = Point(43.7378551, -81.7306819)
loc_buffalo_ny = Point(42.8962094, -78.9470139)
loc_talledega_natlforst = Point(32.95047, -87.393259)
loc_pacific_ocean = Point(0, 5)


def test_get_weather_no_coverage():
    logger.setLevel(logging.DEBUG)
    test_coords = loc_pacific_ocean
    result = get_weather(test_coords._lat, test_coords._lon)

    # Assert that the result is None or matches expected behavior for no coverage
    assert result is None or isinstance(result, dict)
    if isinstance(result, dict):
        assert "coverage" in result
        assert isinstance(result["coverage"], float)
        assert result["coverage"] == 0.0  # Expect 0.0 coverage for the Pacific Ocean


def test_get_weather_invalid_timeseries():
    test_coords = loc_talledega_natlforst
    with pytest.raises(KeyError):
        get_weather(test_coords._lat, test_coords._lon, timeseries_type="invalid")


def test_get_weather1():
    # logger.setLevel(logging.DEBUG)
    test_coords = loc_baystlouis_ms
    weather = get_weather(test_coords._lat, test_coords._lon, date_hurricane_katrina)

    assert isinstance(weather, dict)

    assert "data" in weather
    assert "station" in weather
    assert "coverage" in weather

    assert isinstance(weather["coverage"], float)
    assert 0.0 <= weather["coverage"] <= 1.0

    assert isinstance(weather["data"], dict)
    assert isinstance(weather["station"], dict)

    # confirm that at least one value inside data is a dict
    assert any(isinstance(v, dict) for v in weather["data"].values())

    # test prcp column
    testcol = "prcp"
    assert testcol in weather["data"]

    col_data = weather["data"][testcol]
    assert isinstance(col_data, dict)  # Should be a dict mapping timestamps to values

    # Check that col_data is not empty
    assert len(col_data) > 0

    # Check that the temperature values are numeric (int or float) or None/NaN
    for _timestamp, value in col_data.items():
        # You could allow None or NaN if those exist in your data
        if value is not None:
            assert isinstance(value, int | float)


def test_get_weather2():
    # logger.setLevel(logging.DEBUG)
    test_coords = loc_lansing_mi
    weather = get_weather(test_coords._lat, test_coords._lon, date_hurricane_huron)

    assert isinstance(weather, dict)

    assert "data" in weather
    assert "station" in weather
    assert "coverage" in weather

    assert isinstance(weather["coverage"], float)
    assert 0.0 <= weather["coverage"] <= 1.0

    assert isinstance(weather["data"], dict)
    assert isinstance(weather["station"], dict)

    # confirm that at least one value inside data is a dict
    assert any(isinstance(v, dict) for v in weather["data"].values())

    # test temp column
    testcol = "temp"
    assert testcol in weather["data"]

    col_data = weather["data"][testcol]
    assert isinstance(col_data, dict)  # Should be a dict mapping timestamps to values

    # Check that col_data is not empty
    assert len(col_data) > 0

    # Check that the temperature values are numeric (int or float) or None/NaN
    for _timestamp, value in col_data.items():
        # You could allow None or NaN if those exist in your data
        if value is not None:
            assert isinstance(value, int | float)
