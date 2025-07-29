# tests/test_intraday.py

import os
import pytest
from dotenv import load_dotenv
from alpha_vantage_client import AlphaVantageClient
from functools import partial

# Load .env variables for local dev
load_dotenv()

@pytest.fixture
def client():
    api_key = os.getenv("ALPHA_ADVANTAGE_API_KEY")
    assert api_key, "ALPHA_ADVANTAGE_API_KEY not found in environment"
    return AlphaVantageClient(api_key=api_key)

# def test_intraday_compact(client):
#     result = client.get_time_series_intraday(symbol="AAPL", interval="5min")
#     assert isinstance(result, dict), "Expected result to be a dictionary"
#     assert any("Time Series" in k for k in result.keys()), "Response missing expected time series data"

# def test_get_global_market_status(client):
#     result = client.get_global_market_status()
#     print(result)
#     assert isinstance(result, dict), "Expected result to be a dictionary"

# def test_get_moving_averages(client):
#     result = client.get_moving_average(
#         function="EMA",
#         symbol="IBM",
#         time_period=200,
#         interval="monthly",
#         series_type="high",
#         datatype="csv",
#         slowlimit=0.02,
#     )
#     print(result)
#     assert isinstance(result, (dict, str)), "Expected result to be a dict or str"
# def test_fetchTI(client):
#     # Store the function with pre-filled parameters
#     sma_fetcher = partial(
#         client.fetchTI,
#         "SMA",
#         symbol="AAPL",
#         interval="daily",
#         series_type="open",
#         time_period=20
#     )

    
#     # Call it later
#     sma_data = sma_fetcher()
#     second_sma_data = sma_fetcher(series_type="close")
#     print(str(sma_data)[0:20])
#     print(str(second_sma_data)[0:20])
#     assert isinstance(sma_data, (dict, str)), "Expected result to be a dict or str"

def test_new_setup(client):
    try:
        # response = client.query(
        #     endpoint_name="time_series_daily",
        #     symbol="AAPL",  # Stock symbol for Apple
        #     outputsize="compact",  # Can be "compact" or "full"
        #     datatype="json"  # Can be "json" or "csv"
        # )
        # print(response)  # Print the response
        # details = client.get_available_endpoints(detailed=True) 
        # print(details['ht_dcperiod'])

        print(client.get_available_endpoints(filter_by="gdp", detailed=True))



    except Exception as e:
        print(f"Error: {e}")