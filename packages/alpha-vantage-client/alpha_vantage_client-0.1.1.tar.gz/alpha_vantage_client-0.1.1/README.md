# Alpha Vantage Client

A comprehensive, configuration-driven Python client for Alpha Vantage API with
support for all endpoints including stocks, forex, crypto, commodities, economic
indicators, and Alpha Intelligence features.

## Features

- **Complete API Coverage**: All Alpha Vantage endpoints including premium
  features
- **Configuration-Driven**: Easy-to-use endpoint configuration system
- **Default Parameters**: Set defaults at client initialization for cleaner code
- **Type Safety**: Full type hints and validation
- **Developer-Friendly**: Beautiful output formatting and comprehensive
  documentation
- **Easy Discovery**: Built-in endpoint discovery and filtering

## Supported Endpoints

### 📈 Time Series & Quotes

- Intraday, daily, weekly, monthly time series
- Real-time quotes and bulk quotes
- Market status

### 📊 Technical Indicators

- Moving averages (SMA, EMA, WMA, DEMA, TEMA, etc.)
- Momentum indicators (RSI, MACD, Stochastic, etc.)
- Trend indicators (ADX, Aroon, etc.)
- Volatility indicators (Bollinger Bands, ATR, etc.)
- Volume indicators (OBV, MFI, etc.)
- And many more...

### 🏢 Fundamental Data

- Company overview and financial statements
- Earnings and dividends
- ETF profiles and holdings
- Options data

### 🌍 Economic Indicators

- GDP, inflation, unemployment
- Treasury yields, federal funds rate
- Retail sales, durable goods
- Nonfarm payroll

### 🛢️ Commodities

- Energy (WTI, Brent, Natural Gas)
- Metals (Copper, Aluminum)
- Agriculture (Wheat, Corn, Cotton, Sugar, Coffee)

### 💱 Forex & Crypto

- Currency exchange rates
- Forex time series
- Cryptocurrency data

### 🧠 Alpha Intelligence

- News sentiment analysis
- Earnings call transcripts
- Insider transactions
- Top gainers/losers
- Advanced analytics (fixed and sliding window)

## Installation

```bash
pip install alpha-vantage-client
```

## Quick Start

```python
from alpha_vantage_client import AlphaVantageClient

# Initialize with your API key
client = AlphaVantageClient(
    api_key="YOUR_API_KEY",
    default_symbol="AAPL",
    default_datatype="json"
)

# Get stock data
data = client.query("time_series_daily", symbol="AAPL")

# Get technical indicators
sma_data = client.query("sma", symbol="AAPL", interval="daily", series_type="close", time_period=20)

# Get economic data
gdp_data = client.query("real_gdp", interval="quarterly")

# Get news sentiment
news_data = client.query("news_sentiment", tickers="AAPL,TSLA", topics="technology")
```

## Advanced Usage

### Setting Defaults

```python
client = AlphaVantageClient(
    api_key="YOUR_API_KEY",
    default_symbol="AAPL",
    default_datatype="json",
    default_interval="daily",
    default_series_type="close",
    default_time_period=20
)

# Now you can call methods without specifying common parameters
sma_data = client.query("sma")  # Uses defaults
rsi_data = client.query("rsi")  # Uses defaults
```

### Discovering Endpoints

```python
# Get all available endpoints
all_endpoints = client.get_available_endpoints()

# Get endpoints by category
economic_endpoints = client.get_available_endpoints(category="economic")
tech_indicators = client.get_available_endpoints(category="technical_indicators")

# Search for specific endpoints
gdp_endpoints = client.get_available_endpoints(filter_by="gdp")

# Get detailed information
detailed_info = client.get_available_endpoints(detailed=True, category="economic")
```

### Advanced Analytics

```python
# Fixed window analytics
analytics = client.query("analytics_fixed_window",
                        SYMBOLS="AAPL,MSFT,IBM",
                        RANGE="2023-07-01",
                        INTERVAL="DAILY",
                        CALCULATIONS="MEAN,STDDEV,CORRELATION")

# Sliding window analytics
sliding_analytics = client.query("analytics_sliding_window",
                                SYMBOLS="AAPL,IBM",
                                RANGE="2month",
                                INTERVAL="DAILY",
                                WINDOW_SIZE=20,
                                CALCULATIONS="MEAN,STDDEV(annualized=True)")
```

## Configuration

The client supports extensive configuration options with intelligent defaults:

```python
client = AlphaVantageClient(
    api_key="YOUR_API_KEY",
    # Time series defaults
    default_symbol="AAPL",
    default_interval="daily",
    default_outputsize="compact",
    default_datatype="json",
    
    # Technical indicator defaults
    default_series_type="close",
    default_time_period=20,
    
    # Other defaults
    default_adjusted=True,
    default_extended_hours=False
)
```

### Intelligent Defaults

The client applies defaults intelligently based on each endpoint's validation
rules:

- **Commodities** (sugar, wheat, etc.): No default interval applied (uses API
  default)
- **Economic indicators** (GDP, CPI, etc.): No default interval applied
- **Time series**: Default `interval="daily"` applied
- **Technical indicators**: Default `interval="daily"` and `series_type="close"`
  applied

This prevents validation errors when defaults don't match endpoint requirements.

## Error Handling

The client provides clear error messages and validation:

```python
try:
    data = client.query("sma", symbol="INVALID", interval="invalid")
except ValueError as e:
    print(f"Validation error: {e}")
except RuntimeError as e:
    print(f"API error: {e}")
```

## Development

### Installation for Development

```bash
git clone https://github.com/yourusername/alpha-vantage-client.git
cd alpha-vantage-client
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=alpha_vantage_client
```

### Code Formatting

```bash
black alpha_vantage_client/
flake8 alpha_vantage_client/
mypy alpha_vantage_client/
```

## Documentation

- [Full API Documentation](https://alpha-vantage-client.readthedocs.io/)
- [Alpha Vantage API Reference](https://www.alphavantage.co/documentation/)
- [Changelog](CHANGELOG.md) - See what's new in each version

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## Support

- 📧 Email: your.email@example.com
- 🐛 Issues:
  [GitHub Issues](https://github.com/yourusername/alpha-vantage-client/issues)
- 📖 Documentation:
  [Read the Docs](https://alpha-vantage-client.readthedocs.io/)

## Acknowledgments

- [Alpha Vantage](https://www.alphavantage.co/) for providing the financial data
  APIs
- The Python community for excellent tools and libraries
