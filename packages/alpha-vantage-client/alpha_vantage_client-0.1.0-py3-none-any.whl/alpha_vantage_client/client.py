import requests
import os
from typing import Optional, Dict, Union, Any, List
from dataclasses import dataclass, field
from datetime import date
from dateutil import parser


def normalize_date(user_input: str) -> str:
    """Normalize date input to ISO format with validation"""
    try:
        parsed_date = parser.parse(user_input).date()
        if parsed_date >= date(2008, 1, 1):
            return parsed_date.isoformat()
        return "Error: Date must be after January 1, 2008."
    except Exception as e:
        return f"Error: Could not parse date. ({e})"


@dataclass
class APIEndpoint:
    """Configuration for an API endpoint"""
    function: str
    required_params: List[str] = field(default_factory=list)
    optional_params: List[str] = field(default_factory=list)
    validation_rules: Dict[str, set] = field(default_factory=dict)
    param_transforms: Dict[str, callable] = field(default_factory=dict)
    conditional_params: Dict[str, Dict] = field(default_factory=dict)  # For conditional parameter inclusion


class AlphaVantageClient:
    """Configuration-driven AlphaVantage client with comprehensive endpoint support"""
    BASE_URL = "https://www.alphavantage.co/query"
    
    # Define all endpoints in one place
    ENDPOINTS = {
        # Time Series Endpoints
        "time_series_intraday": APIEndpoint(
            function="TIME_SERIES_INTRADAY",
            required_params=["symbol", "interval"],
            optional_params=["adjusted", "extended_hours", "month", "outputsize", "datatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min"}
            },
            param_transforms={
                "adjusted": lambda x: str(x).lower() if x is not None else None,
                "extended_hours": lambda x: str(x).lower() if x is not None else None,
            }
        ),
        "time_series_daily": APIEndpoint(
            function="TIME_SERIES_DAILY",
            required_params=["symbol"],
            optional_params=["outputsize", "datatype"],
        ),
        "time_series_daily_adjusted": APIEndpoint(
            function="TIME_SERIES_DAILY_ADJUSTED",
            required_params=["symbol"],
            optional_params=["outputsize", "datatype"],
        ),
        "time_series_weekly": APIEndpoint(
            function="TIME_SERIES_WEEKLY",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        "time_series_weekly_adjusted": APIEndpoint(
            function="TIME_SERIES_WEEKLY_ADJUSTED",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        "time_series_monthly": APIEndpoint(
            function="TIME_SERIES_MONTHLY",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        "time_series_monthly_adjusted": APIEndpoint(
            function="TIME_SERIES_MONTHLY_ADJUSTED",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        
        # Quote Endpoints
        "global_quote": APIEndpoint(
            function="GLOBAL_QUOTE",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        "realtime_bulk_quotes": APIEndpoint(
            function="REALTIME_BULK_QUOTES",
            required_params=["symbol"],
            optional_params=["datatype"],
            param_transforms={
                "symbol": lambda x: ",".join(x) if isinstance(x, list) else x,
            }
        ),
        
        # Market Status
        "market_status": APIEndpoint(
            function="MARKET_STATUS",
            required_params=[],
            optional_params=[],
        ),
        
        # Options
        "historical_options": APIEndpoint(
            function="HISTORICAL_OPTIONS",
            required_params=["symbol"],
            optional_params=["date", "contract", "datatype", "require_greeks"],
            param_transforms={
                "date": lambda x: normalize_date(x) if x else None,
                "require_greeks": lambda x: str(x).lower() if x is not None else None,
            }
        ),
        "realtime_options": APIEndpoint(
            function="REALTIME_OPTIONS",
            required_params=["symbol"],
            optional_params=["contract", "datatype", "require_greeks"],
            param_transforms={
                "require_greeks": lambda x: str(x).lower() if x is not None else None,
            }
        ),
        

        # Fundamental Data
        "company_overview": APIEndpoint(
            function="OVERVIEW",
            required_params=["function", "symbol"],
        ),
        "etf_profile_holding": APIEndpoint(
            function="ETF_PROFILE",
            required_params=["symbol"],
        ),
        "dividends": APIEndpoint(
            function="DIVIDENDS",
            required_params=[ "symbol"],
        ),
        "income_statement": APIEndpoint(
            function="INCOME_STATEMENT",
            required_params=[ "symbol"],
        ),
        "balance_sheet": APIEndpoint(
            function="BALANCE_SHEET",
            required_params=[ "symbol"],
        ),
        "cash_flow": APIEndpoint(
            function="CASH_FLOW",
            required_params=["symbol"],
        ),
        "earnings": APIEndpoint(
            function="EARNINGS",
            required_params=["symbol"],
        ),
        
        "listing_status": APIEndpoint(
            function="LISTING_STATUS",
            required_params=[],
            optional_params=["date", "state", "datatype"],
            validation_rules={
                "state": {"active", "delisted"}
            },
            param_transforms={
                "date": lambda x: normalize_date(x) if x else None,
            }
        ),
        "earnings_calendar": APIEndpoint(
            function="EARNINGS_CALENDAR",
            required_params=[],
            optional_params=["symbol", "horizon", "datatype"],
            validation_rules={
                "horizon": {"3month", "6month", "12month"}
            }
        ),
        "ipo_calendar": APIEndpoint(
            function="IPO_CALENDAR",
            required_params=[],
        ),
        
        # Foreign Exchange (FX) Endpoints
        "currency_exchange_rate": APIEndpoint(
            function="CURRENCY_EXCHANGE_RATE",
            required_params=["from_currency", "to_currency"],
            optional_params=["datatype"],
        ),
        "fx_intraday": APIEndpoint(
            function="FX_INTRADAY",
            required_params=["from_symbol", "to_symbol", "interval"],
            optional_params=["outputsize", "datatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min"}
            }
        ),
        "fx_daily": APIEndpoint(
            function="FX_DAILY",
            required_params=["from_symbol", "to_symbol"],
            optional_params=["outputsize", "datatype"],
        ),
        "fx_weekly": APIEndpoint(
            function="FX_WEEKLY",
            required_params=["from_symbol", "to_symbol"],
            optional_params=["datatype"],
        ),
        "fx_monthly": APIEndpoint(
            function="FX_MONTHLY",
            required_params=["from_symbol", "to_symbol"],
            optional_params=["datatype"],
        ),
        
        # Cryptocurrency Endpoints
        "crypto_intraday": APIEndpoint(
            function="CRYPTO_INTRADAY",
            required_params=["symbol", "market", "interval"],
            optional_params=["outputsize", "datatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min"}
            }
        ),
        "digital_currency_daily": APIEndpoint(
            function="DIGITAL_CURRENCY_DAILY",
            required_params=["symbol", "market"],
            optional_params=["datatype"],
        ),
        "digital_currency_weekly": APIEndpoint(
            function="DIGITAL_CURRENCY_WEEKLY",
            required_params=["symbol", "market"],
            optional_params=["datatype"],
        ),
        "digital_currency_monthly": APIEndpoint(
            function="DIGITAL_CURRENCY_MONTHLY",
            required_params=["symbol", "market"],
            optional_params=["datatype"],
        ),
        
        # Moving Averages
        "sma": APIEndpoint(
            function="SMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            },
            conditional_params={
                "month": {"condition": lambda params: params.get("interval") in {"1min", "5min", "15min", "30min", "60min"}}
            }
        ),
        "ema": APIEndpoint(
            function="EMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            },
            conditional_params={
                "month": {"condition": lambda params: params.get("interval") in {"1min", "5min", "15min", "30min", "60min"}}
            }
        ),
        "wma": APIEndpoint(
            function="WMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "dema": APIEndpoint(
            function="DEMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "tema": APIEndpoint(
            function="TEMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "trima": APIEndpoint(
            function="TRIMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "kama": APIEndpoint(
            function="KAMA",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "mama": APIEndpoint(
            function="MAMA",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "fastlimit", "slowlimit", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "t3": APIEndpoint(
            function="T3",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        
        # Momentum Indicators
        "rsi": APIEndpoint(
            function="RSI",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "mom": APIEndpoint(
            function="MOM",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "roc": APIEndpoint(
            function="ROC",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "rocr": APIEndpoint(
            function="ROCR",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "cmo": APIEndpoint(
            function="CMO",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "willr": APIEndpoint(
            function="WILLR",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "stoch": APIEndpoint(
            function="STOCH",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month", "fastkperiod", "slowkperiod", "slowdperiod", "slowkmatype", "slowdmatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "stochf": APIEndpoint(
            function="STOCHF",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month", "fastkperiod", "fastdperiod", "fastdmatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "stochrsi": APIEndpoint(
            function="STOCHRSI",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month", "fastkperiod", "fastdperiod", "fastdmatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        
        # Trend Indicators
        "adx": APIEndpoint(
            function="ADX",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "adxr": APIEndpoint(
            function="ADXR",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "plus_di": APIEndpoint(
            function="PLUS_DI",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "minus_di": APIEndpoint(
            function="MINUS_DI",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "plus_dm": APIEndpoint(
            function="PLUS_DM",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "minus_dm": APIEndpoint(
            function="MINUS_DM",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "dx": APIEndpoint(
            function="DX",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "aroon": APIEndpoint(
            function="AROON",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "aroonosc": APIEndpoint(
            function="AROONOSC",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "macd": APIEndpoint(
            function="MACD",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month", "fastperiod", "slowperiod", "signalperiod"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "macdext": APIEndpoint(
            function="MACDEXT",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month", "fastperiod", "slowperiod", "signalperiod", "fastmatype", "slowmatype", "signalmatype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ppo": APIEndpoint(
            function="PPO",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month", "fastperiod", "slowperiod", "matype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "apo": APIEndpoint(
            function="APO",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month", "fastperiod", "slowperiod", "matype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "midprice": APIEndpoint(
            function="MIDPRICE",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        
        # Volatility Indicators
        "bbands": APIEndpoint(
            function="BBANDS",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month", "nbdevup", "nbdevdn", "matype"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "atr": APIEndpoint(
            function="ATR",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "natr": APIEndpoint(
            function="NATR",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "trange": APIEndpoint(
            function="TRANGE",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        
        # Volume Indicators
        "obv": APIEndpoint(
            function="OBV",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "ad": APIEndpoint(
            function="AD",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "adosc": APIEndpoint(
            function="ADOSC",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month", "fastperiod", "slowperiod"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "mfi": APIEndpoint(
            function="MFI",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        
        # Oscillator Indicators
        "trix": APIEndpoint(
            function="TRIX",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ultosc": APIEndpoint(
            function="ULTOSC",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month", "timeperiod1", "timeperiod2", "timeperiod3"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "cci": APIEndpoint(
            function="CCI",
            required_params=["symbol", "interval", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "bop": APIEndpoint(
            function="BOP",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        
        # Hilbert Transform Indicators
        "ht_trendline": APIEndpoint(
            function="HT_TRENDLINE",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ht_sine": APIEndpoint(
            function="HT_SINE",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ht_trendmode": APIEndpoint(
            function="HT_TRENDMODE",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ht_dcperiod": APIEndpoint(
            function="HT_DCPERIOD",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ht_dcphase": APIEndpoint(
            function="HT_DCPHASE",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        "ht_phasor": APIEndpoint(
            function="HT_PHASOR",
            required_params=["symbol", "interval", "series_type"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        
        # Miscellaneous Indicators
        "vwap": APIEndpoint(
            function="VWAP",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min"}
            }
        ),
        "sar": APIEndpoint(
            function="SAR",
            required_params=["symbol", "interval"],
            optional_params=["datatype", "month", "acceleration", "maximum"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"}
            }
        ),
        "midpoint": APIEndpoint(
            function="MIDPOINT",
            required_params=["symbol", "interval", "series_type", "time_period"],
            optional_params=["datatype", "month"],
            validation_rules={
                "interval": {"1min", "5min", "15min", "30min", "60min", "daily", "weekly", "monthly"},
                "series_type": {"open", "close", "high", "low"}
            }
        ),
        
        # Economic Indicators
        "real_gdp": APIEndpoint(
            function="REAL_GDP",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"quarterly", "annual"}
            }
        ),
        "real_gdp_per_capita": APIEndpoint(
            function="REAL_GDP_PER_CAPITA",
            required_params=[],
            optional_params=["datatype"],
        ),
        "treasury_yield": APIEndpoint(
            function="TREASURY_YIELD",
            required_params=[],
            optional_params=["interval", "maturity", "datatype"],
            validation_rules={
                "interval": {"daily", "weekly", "monthly"},
                "maturity": {"3month", "2year", "5year", "7year", "10year", "30year"}
            }
        ),
        "federal_funds_rate": APIEndpoint(
            function="FEDERAL_FUNDS_RATE",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"daily", "weekly", "monthly"}
            }
        ),
        "cpi": APIEndpoint(
            function="CPI",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "semiannual"}
            }
        ),
        "inflation": APIEndpoint(
            function="INFLATION",
            required_params=[],
            optional_params=["datatype"],
        ),
        "retail_sales": APIEndpoint(
            function="RETAIL_SALES",
            required_params=[],
            optional_params=["datatype"],
        ),
        "durables": APIEndpoint(
            function="DURABLES",
            required_params=[],
            optional_params=["datatype"],
        ),
        "unemployment": APIEndpoint(
            function="UNEMPLOYMENT",
            required_params=[],
            optional_params=["datatype"],
        ),
        "nonfarm_payroll": APIEndpoint(
            function="NONFARM_PAYROLL",
            required_params=[],
            optional_params=["datatype"],
        ),
        
        # Commodities Endpoints
        "wti": APIEndpoint(
            function="WTI",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"daily", "weekly", "monthly"}
            }
        ),
        "brent": APIEndpoint(
            function="BRENT",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"daily", "weekly", "monthly"}
            }
        ),
        "natural_gas": APIEndpoint(
            function="NATURAL_GAS",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"daily", "weekly", "monthly"}
            }
        ),
        "copper": APIEndpoint(
            function="COPPER",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "aluminum": APIEndpoint(
            function="ALUMINUM",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "wheat": APIEndpoint(
            function="WHEAT",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "corn": APIEndpoint(
            function="CORN",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "cotton": APIEndpoint(
            function="COTTON",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "sugar": APIEndpoint(
            function="SUGAR",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "coffee": APIEndpoint(
            function="COFFEE",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "all_commodities": APIEndpoint(
            function="ALL_COMMODITIES",
            required_params=[],
            optional_params=["interval", "datatype"],
            validation_rules={
                "interval": {"monthly", "quarterly", "annual"}
            }
        ),
        "news_sentiment": APIEndpoint(
            function="NEWS_SENTIMENT",
            required_params=[],
            optional_params=["tickers", "topics", "time_from", "time_to", "sort", "limit", "datatype"],
            validation_rules={
                "sort": {"LATEST", "EARLIEST", "RELEVANCE"},
                "topics": {"blockchain", "earnings", "ipo", "mergers_and_acquisitions", "financial_markets", 
                          "economy_fiscal", "economy_monetary", "economy_macro", "energy_transportation", 
                          "finance", "life_sciences", "manufacturing", "real_estate", "retail_wholesale", "technology"}
            }
        ),
        "earnings_call_transcript": APIEndpoint(
            function="EARNINGS_CALL_TRANSCRIPT",
            required_params=["symbol", "quarter"],
            optional_params=["datatype"],
            validation_rules={
                "quarter": {"string"}  # Format: YYYYQM (e.g., 2024Q1)
            }
        ),
        "top_gainers_losers": APIEndpoint(
            function="TOP_GAINERS_LOSERS",
            required_params=[],
            optional_params=["datatype"],
        ),
        "insider_transactions": APIEndpoint(
            function="INSIDER_TRANSACTIONS",
            required_params=["symbol"],
            optional_params=["datatype"],
        ),
        "analytics_fixed_window": APIEndpoint(
            function="ANALYTICS_FIXED_WINDOW",
            required_params=["SYMBOLS", "RANGE", "INTERVAL", "CALCULATIONS"],
            optional_params=["OHLC", "datatype"],
            validation_rules={
                "INTERVAL": {"1min", "5min", "15min", "30min", "60min", "DAILY", "WEEKLY", "MONTHLY"},
                "OHLC": {"open", "high", "low", "close"},
                "CALCULATIONS": {"MIN", "MAX", "MEAN", "MEDIAN", "CUMULATIVE_RETURN", "VARIANCE", 
                                "STDDEV", "MAX_DRAWDOWN", "HISTOGRAM", "AUTOCORRELATION", "COVARIANCE", "CORRELATION"}
            }
        ),
        "analytics_sliding_window": APIEndpoint(
            function="ANALYTICS_SLIDING_WINDOW",
            required_params=["SYMBOLS", "RANGE", "INTERVAL", "WINDOW_SIZE", "CALCULATIONS"],
            optional_params=["OHLC", "datatype"],
            validation_rules={
                "INTERVAL": {"1min", "5min", "15min", "30min", "60min", "DAILY", "WEEKLY", "MONTHLY"},
                "OHLC": {"open", "high", "low", "close"},
                "WINDOW_SIZE": {"integer"},  # Minimum 10
                "CALCULATIONS": {"MEAN", "MEDIAN", "CUMULATIVE_RETURN", "VARIANCE", "STDDEV", "COVARIANCE", "CORRELATION"}
            }
        ),
    }

    def __init__(self, api_key: str = None, **defaults):
        """Initialize with API key and defaults"""
        self.api_key = api_key or os.getenv("ALPHA_VANTAGE_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided")
        
        # Set defaults
        self.defaults = {
            'datatype': 'json',
            'outputsize': 'compact',
            'time_period': 60,
            'interval': 'daily',
            'series_type': 'close',
            **defaults
        }

    def _resolve_params(self, endpoint: APIEndpoint, **kwargs) -> Dict:
        """Resolve parameters with defaults and validation"""
        params = {"function": endpoint.function}
        
        # Merge with defaults
        merged_params = {**self.defaults, **kwargs}
        
        # Check required parameters
        for param in endpoint.required_params:
            if param not in merged_params or merged_params[param] is None:
                raise ValueError(f"Required parameter '{param}' not provided")
            params[param] = merged_params[param]
        
        # Add optional parameters
        for param in endpoint.optional_params:
            if param in merged_params and merged_params[param] is not None:
                # Check conditional parameters
                if param in endpoint.conditional_params:
                    condition = endpoint.conditional_params[param]["condition"]
                    if not condition(merged_params):
                        continue
                params[param] = merged_params[param]
        
        # Validate parameters
        for param, valid_values in endpoint.validation_rules.items():
            if param in params and params[param] not in valid_values:
                raise ValueError(f"Invalid {param}: {params[param]}. Must be one of {valid_values}")
        
        # Apply transformations
        for param, transform in endpoint.param_transforms.items():
            if param in params:
                params[param] = transform(params[param])
        
        # Remove None values
        return {k: v for k, v in params.items() if v is not None}

    def _request(self, params: Dict) -> Union[Dict, str]:
        """Make API request"""
        params["apikey"] = self.api_key
        response = requests.get(self.BASE_URL, params=params)
        
        if not response.ok:
            raise RuntimeError(f"Alpha Vantage API error: {response.status_code} {response.text}")
        
        datatype = params.get("datatype", "json")
        return response.json() if datatype == "json" else response.text

    def _call_endpoint(self, endpoint_name: str, **kwargs) -> Union[Dict, str]:
        """Generic method to call any endpoint"""
        if endpoint_name not in self.ENDPOINTS:
            raise ValueError(f"Unknown endpoint: {endpoint_name}")
        
        endpoint = self.ENDPOINTS[endpoint_name]
        params = self._resolve_params(endpoint, **kwargs)
        return self._request(params)

    def query(self, endpoint_name: str, **kwargs) -> Union[Dict, str]:
        """Public method to call any endpoint"""
        return self._call_endpoint(endpoint_name, **kwargs)

    def get_available_endpoints(self, detailed: bool = False, filter_by: Optional[str] = None, category: Optional[str] = None, pretty_print: bool = True) -> Union[List[str], Dict]:
        """
        Return a list of available endpoint names or detailed endpoint information.
        
        Args:
            detailed (bool): If True, return a dictionary with endpoint details including
                            required and optional parameters and validation rules.
            filter_by (str): Filter endpoints by name (partial match, case-insensitive)
            category (str): Filter by category (time_series, technical_indicators, fundamental, 
                           economic, commodities, forex, crypto, etc.)
            pretty_print (bool): If True and detailed=True, return formatted string instead of dict
        
        Returns:
            Union[List[str], Dict, str]: List of endpoint names, dictionary with endpoint details, or formatted string.
        """
        # Define endpoint categories for better organization
        endpoint_categories = {
            "time_series": [
                "time_series_intraday", "time_series_daily", "time_series_daily_adjusted",
                "time_series_weekly", "time_series_weekly_adjusted",
                "time_series_monthly", "time_series_monthly_adjusted"
            ],
            "quotes": ["global_quote", "realtime_bulk_quotes"],
            "market_status": ["market_status"],
            "options": ["historical_options", "realtime_options"],
            "fundamental": [
                "company_overview", "etf_profile_holding", "dividends", "income_statement",
                "balance_sheet", "cash_flow", "earnings"
            ],
            "technical_indicators": [
                "sma", "ema", "wma", "dema", "tema", "trima", "kama", "mama", "t3",
                "rsi", "mom", "roc", "rocr", "cmo", "willr", "stoch", "stochf", "stochrsi",
                "adx", "adxr", "plus_di", "minus_di", "plus_dm", "minus_dm", "dx",
                "aroon", "aroonosc", "macd", "macdext", "ppo", "apo", "midprice",
                "bbands", "atr", "natr", "trange", "obv", "ad", "adosc", "mfi",
                "trix", "ultosc", "cci", "bop", "ht_trendline", "ht_sine", "ht_trendmode",
                "ht_dcperiod", "ht_dcphase", "ht_phasor", "vwap", "sar", "midpoint"
            ],
            "economic": [
                "real_gdp", "real_gdp_per_capita", "treasury_yield", "federal_funds_rate",
                "cpi", "inflation", "retail_sales", "durables", "unemployment", "nonfarm_payroll"
            ],
            "commodities": [
                "wti", "brent", "natural_gas", "copper", "aluminum", "wheat", "corn",
                "cotton", "sugar", "coffee", "all_commodities"
            ],
            "forex": [
                "currency_exchange_rate", "fx_intraday", "fx_daily", "fx_weekly", "fx_monthly"
            ],
            "crypto": [
                "crypto_intraday", "digital_currency_daily", "digital_currency_weekly", "digital_currency_monthly"
            ],
            "listing": ["listing_status", "earnings_calendar", "ipo_calendar"],
            "alpha_intelligence": ["news_sentiment", "earnings_call_transcript", "top_gainers_losers", 
                                 "insider_transactions", "analytics_fixed_window", "analytics_sliding_window"]
        }
        
        # Get all available endpoints
        all_endpoints = list(self.ENDPOINTS.keys())
        
        # Apply filters
        filtered_endpoints = all_endpoints
        
        if filter_by:
            filter_by_lower = filter_by.lower()
            filtered_endpoints = [ep for ep in all_endpoints if filter_by_lower in ep.lower()]
        
        if category:
            category_lower = category.lower()
            if category_lower in endpoint_categories:
                filtered_endpoints = [ep for ep in filtered_endpoints if ep in endpoint_categories[category_lower]]
            else:
                # If category not found, return empty list
                filtered_endpoints = []
        
        if not detailed:
            if pretty_print and filtered_endpoints:
                return self._format_simple_list(filtered_endpoints, filter_by, category)
            return filtered_endpoints
        
        # Return detailed information with better formatting
        result = {}
        
        for endpoint_name in filtered_endpoints:
            endpoint = self.ENDPOINTS[endpoint_name]
            
            # Find which category this endpoint belongs to
            endpoint_category = "other"
            for cat, endpoints in endpoint_categories.items():
                if endpoint_name in endpoints:
                    endpoint_category = cat
                    break
            
            result[endpoint_name] = {
                "category": endpoint_category,
                "function": endpoint.function,
                "description": self._get_endpoint_description(endpoint_name),
                "required_params": endpoint.required_params,
                "optional_params": endpoint.optional_params,
                "validation_rules": endpoint.validation_rules,
                "example_usage": self._get_example_usage(endpoint_name, endpoint)
            }
        
        if pretty_print:
            return self._format_detailed_output(result, filter_by, category)
        
        return result
    
    def _format_simple_list(self, endpoints: List[str], filter_by: Optional[str] = None, category: Optional[str] = None) -> str:
        """Format a simple list of endpoints for pretty printing"""
        if not endpoints:
            return "No endpoints found."
        
        # Group by category for better organization
        endpoint_categories = {
            "time_series": ["time_series_intraday", "time_series_daily", "time_series_daily_adjusted",
                           "time_series_weekly", "time_series_weekly_adjusted",
                           "time_series_monthly", "time_series_monthly_adjusted"],
            "quotes": ["global_quote", "realtime_bulk_quotes"],
            "market_status": ["market_status"],
            "options": ["historical_options", "realtime_options"],
            "fundamental": ["company_overview", "etf_profile_holding", "dividends", "income_statement",
                           "balance_sheet", "cash_flow", "earnings"],
            "technical_indicators": ["sma", "ema", "wma", "dema", "tema", "trima", "kama", "mama", "t3",
                                   "rsi", "mom", "roc", "rocr", "cmo", "willr", "stoch", "stochf", "stochrsi",
                                   "adx", "adxr", "plus_di", "minus_di", "plus_dm", "minus_dm", "dx",
                                   "aroon", "aroonosc", "macd", "macdext", "ppo", "apo", "midprice",
                                   "bbands", "atr", "natr", "trange", "obv", "ad", "adosc", "mfi",
                                   "trix", "ultosc", "cci", "bop", "ht_trendline", "ht_sine", "ht_trendmode",
                                   "ht_dcperiod", "ht_dcphase", "ht_phasor", "vwap", "sar", "midpoint"],
            "economic": ["real_gdp", "real_gdp_per_capita", "treasury_yield", "federal_funds_rate",
                        "cpi", "inflation", "retail_sales", "durables", "unemployment", "nonfarm_payroll"],
            "commodities": ["wti", "brent", "natural_gas", "copper", "aluminum", "wheat", "corn",
                           "cotton", "sugar", "coffee", "all_commodities"],
            "forex": ["currency_exchange_rate", "fx_intraday", "fx_daily", "fx_weekly", "fx_monthly"],
            "crypto": ["crypto_intraday", "digital_currency_daily", "digital_currency_weekly", "digital_currency_monthly"],
            "listing": ["listing_status", "earnings_calendar", "ipo_calendar"],
            "alpha_intelligence": ["news_sentiment", "earnings_call_transcript", "top_gainers_losers", 
                                 "insider_transactions", "analytics_fixed_window", "analytics_sliding_window"]
        }
        
        # Group endpoints by category
        categorized = {}
        for endpoint in endpoints:
            for cat, cat_endpoints in endpoint_categories.items():
                if endpoint in cat_endpoints:
                    if cat not in categorized:
                        categorized[cat] = []
                    categorized[cat].append(endpoint)
                    break
            else:
                if "other" not in categorized:
                    categorized["other"] = []
                categorized["other"].append(endpoint)
        
        # Build output
        output = []
        
        # Header
        if filter_by:
            output.append(f"📋 Endpoints matching '{filter_by}':")
        elif category:
            output.append(f"📋 Endpoints in category '{category}':")
        else:
            output.append("📋 All Available Endpoints:")
        
        output.append("=" * 60)
        
        # Display by category
        for cat, cat_endpoints in categorized.items():
            if cat_endpoints:
                output.append(f"\n🔹 {cat.replace('_', ' ').title()} ({len(cat_endpoints)}):")
                for endpoint in sorted(cat_endpoints):
                    output.append(f"   • {endpoint}")
        
        output.append(f"\n📊 Total: {len(endpoints)} endpoints")
        
        return "\n".join(output)
    
    def _format_detailed_output(self, result: Dict, filter_by: Optional[str] = None, category: Optional[str] = None) -> str:
        """Format detailed endpoint information for pretty printing"""
        if not result:
            return "No endpoints found."
        
        output = []
        
        # Header
        if filter_by:
            output.append(f"📋 Detailed Endpoints matching '{filter_by}':")
        elif category:
            output.append(f"📋 Detailed Endpoints in category '{category}':")
        else:
            output.append("📋 All Available Endpoints (Detailed):")
        
        output.append("=" * 80)
        
        # Group by category
        categorized = {}
        for endpoint_name, details in result.items():
            cat = details["category"]
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append((endpoint_name, details))
        
        # Display by category
        for cat, endpoints in categorized.items():
            if endpoints:
                output.append(f"\n🔹 {cat.replace('_', ' ').title()} ({len(endpoints)}):")
                output.append("-" * 50)
                
                for endpoint_name, details in sorted(endpoints):
                    output.append(f"\n📌 {endpoint_name}")
                    output.append(f"   Description: {details['description']}")
                    output.append(f"   Function: {details['function']}")
                    
                    if details['required_params']:
                        output.append(f"   Required: {', '.join(details['required_params'])}")
                    else:
                        output.append("   Required: None")
                    
                    if details['optional_params']:
                        output.append(f"   Optional: {', '.join(details['optional_params'])}")
                    
                    if details['validation_rules']:
                        output.append("   Validation Rules:")
                        for param, valid_values in details['validation_rules'].items():
                            output.append(f"     {param}: {', '.join(sorted(valid_values))}")
                    
                    output.append(f"   Example: {details['example_usage']}")
                    output.append("")
        
        output.append(f"📊 Total: {len(result)} endpoints")
        
        return "\n".join(output)
    
    def _get_endpoint_description(self, endpoint_name: str) -> str:
        """Get a human-readable description for an endpoint"""
        descriptions = {
            "time_series_intraday": "Intraday time series for stocks",
            "time_series_daily": "Daily time series for stocks",
            "time_series_daily_adjusted": "Daily adjusted time series for stocks",
            "time_series_weekly": "Weekly time series for stocks",
            "time_series_weekly_adjusted": "Weekly adjusted time series for stocks",
            "time_series_monthly": "Monthly time series for stocks",
            "time_series_monthly_adjusted": "Monthly adjusted time series for stocks",
            "global_quote": "Real-time stock quote",
            "realtime_bulk_quotes": "Bulk real-time quotes for multiple symbols",
            "market_status": "Global market status",
            "historical_options": "Historical options data",
            "realtime_options": "Real-time options data",
            "company_overview": "Company overview and fundamentals",
            "etf_profile_holding": "ETF profile and holdings",
            "dividends": "Company dividend data",
            "income_statement": "Company income statement",
            "balance_sheet": "Company balance sheet",
            "cash_flow": "Company cash flow statement",
            "earnings": "Company earnings data",
            "sma": "Simple Moving Average technical indicator",
            "ema": "Exponential Moving Average technical indicator",
            "rsi": "Relative Strength Index technical indicator",
            "macd": "MACD technical indicator",
            "bbands": "Bollinger Bands technical indicator",
            "real_gdp": "Real GDP data",
            "real_gdp_per_capita": "Real GDP per capita data",
            "treasury_yield": "Treasury yield data",
            "federal_funds_rate": "Federal funds rate data",
            "cpi": "Consumer Price Index data",
            "inflation": "Inflation rate data",
            "retail_sales": "Retail sales data",
            "durables": "Durable goods orders data",
            "unemployment": "Unemployment rate data",
            "nonfarm_payroll": "Nonfarm payroll employment data",
            "wti": "West Texas Intermediate crude oil prices",
            "brent": "Brent crude oil prices",
            "natural_gas": "Natural gas prices",
            "copper": "Global copper prices",
            "aluminum": "Global aluminum prices",
            "wheat": "Global wheat prices",
            "corn": "Global corn prices",
            "cotton": "Global cotton prices",
            "sugar": "Global sugar prices",
            "coffee": "Global coffee prices",
            "all_commodities": "Global commodity price index",
            "currency_exchange_rate": "Currency exchange rates",
            "fx_intraday": "Forex intraday time series",
            "fx_daily": "Forex daily time series",
            "fx_weekly": "Forex weekly time series",
            "fx_monthly": "Forex monthly time series",
            "crypto_intraday": "Cryptocurrency intraday time series",
            "digital_currency_daily": "Cryptocurrency daily time series",
            "digital_currency_weekly": "Cryptocurrency weekly time series",
            "digital_currency_monthly": "Cryptocurrency monthly time series",
            "listing_status": "Stock listing status",
            "earnings_calendar": "Earnings calendar",
            "ipo_calendar": "IPO calendar",
            "news_sentiment": "News sentiment data",
            "earnings_call_transcript": "Earnings call transcript data",
            "top_gainers_losers": "Top gainers and losers data",
            "insider_transactions": "Insider transactions data",
            "analytics_fixed_window": "Fixed window analytics data",
            "analytics_sliding_window": "Sliding window analytics data"
        }
        return descriptions.get(endpoint_name, "No description available")
    
    def _get_example_usage(self, endpoint_name: str, endpoint) -> str:
        """Generate example usage for an endpoint"""
        examples = {
            "time_series_intraday": "client.query('time_series_intraday', symbol='AAPL', interval='5min')",
            "global_quote": "client.query('global_quote', symbol='AAPL')",
            "sma": "client.query('sma', symbol='AAPL', interval='daily', series_type='close', time_period=20)",
            "real_gdp": "client.query('real_gdp', interval='quarterly')",
            "wti": "client.query('wti', interval='monthly')",
            "currency_exchange_rate": "client.query('currency_exchange_rate', from_currency='USD', to_currency='EUR')",
            "crypto_intraday": "client.query('crypto_intraday', symbol='BTC', market='USD', interval='5min')",
            "news_sentiment": "client.query('news_sentiment', tickers='AAPL,TSLA')",
            "earnings_call_transcript": "client.query('earnings_call_transcript', symbol='AAPL', quarter='2023Q1')",
            "top_gainers_losers": "client.query('top_gainers_losers')",
            "insider_transactions": "client.query('insider_transactions', symbol='AAPL')",
            "analytics_fixed_window": "client.query('analytics_fixed_window', symbol='AAPL')",
            "analytics_sliding_window": "client.query('analytics_sliding_window', symbol='AAPL')"
        }
        return examples.get(endpoint_name, f"client.query('{endpoint_name}')")
