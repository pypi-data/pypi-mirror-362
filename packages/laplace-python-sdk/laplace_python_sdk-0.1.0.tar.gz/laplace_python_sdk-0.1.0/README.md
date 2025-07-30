# Laplace Python SDK

[![PyPI version](https://badge.fury.io/py/laplace-python-sdk.svg)](https://badge.fury.io/py/laplace-python-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/laplace-python-sdk.svg)](https://pypi.org/project/laplace-python-sdk/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

The official Python SDK for the Laplace stock data platform. Get easy access to stock data, collections, financials, funds, and AI-powered insights.

## Features

- 🚀 **Easy to use**: Simple, intuitive API
- 📊 **Comprehensive data**: Stocks, collections, financials, funds, and AI insights
- 🔧 **Well-typed**: Full TypeScript-style typing with Pydantic models
- 🧪 **Well-tested**: Comprehensive test coverage with real API integration
- 🌍 **Multi-region**: Support for US and Turkish markets
- ⚡ **Fast**: Built on httpx for high performance

## Installation

```bash
pip install laplace-python-sdk
```

## Quick Start

```python
from laplace import LaplaceClient

# Initialize the client
client = LaplaceClient(api_key="your-api-key")

# Get stock details
stock = client.stocks.get_detail_by_symbol(symbol="AAPL", region="us")
print(f"{stock.name}: {stock.description}")

# Get all stocks in a region
stocks = client.stocks.get_all(region="us", page=1, page_size=10)
for stock in stocks:
    print(f"{stock.symbol}: {stock.name}")

# Get collections
collections = client.collections.get_collections(region="tr", locale="en")
for collection in collections:
    print(f"{collection.title}: {collection.num_stocks} stocks")

# Get collection details
collection_detail = client.collections.get_collection_detail(
    collection_id="620f455a0187ade00bb0d55f", 
    region="tr"
)
print(f"Stocks in {collection_detail.title}:")
for stock in collection_detail.stocks:
    print(f"  {stock.symbol}: {stock.name}")
```

## API Reference

### Stocks Client

```python
# Get all stocks with pagination
stocks = client.stocks.get_all(region="us", page=1, page_size=10)

# Get stock detail by symbol
stock = client.stocks.get_detail_by_symbol(symbol="AAPL", region="us", asset_class="equity")

# Get stock detail by ID
stock = client.stocks.get_detail_by_id(stock_id="stock-id", locale="en")

# Get historical prices
prices = client.stocks.get_price(region="us", symbols=["AAPL", "GOOGL"], keys=["1D", "1W"])

# Get historical prices with custom interval
from datetime import datetime
from laplace.stocks import HistoricalPriceInterval

prices = client.stocks.get_price_with_interval(
    symbol="AAPL",
    region="us", 
    from_date=datetime(2024, 1, 1),
    to_date=datetime(2024, 1, 31),
    interval=HistoricalPriceInterval.ONE_DAY
)

# Get tick rules (Turkey only)
rules = client.stocks.get_tick_rules(region="tr")

# Get restrictions (Turkey only)
restrictions = client.stocks.get_restrictions(region="tr")
```

### Collections Client

```python
# Get all collections
collections = client.collections.get_collections(region="tr", locale="en")

# Get collection detail
detail = client.collections.get_collection_detail(collection_id="id", region="tr")

# Get themes
themes = client.collections.get_themes(region="tr", locale="en")

# Get theme detail
theme_detail = client.collections.get_theme_detail(theme_id="id", region="tr")

# Get industries
industries = client.collections.get_industries(region="tr", locale="en")

# Get industry detail
industry_detail = client.collections.get_industry_detail(industry_id="id", region="tr")

# Get sectors
sectors = client.collections.get_sectors(region="tr", locale="en")

# Get sector detail
sector_detail = client.collections.get_sector_detail(sector_id="id", region="tr")
```

## Supported Regions

- **US**: United States stock market
- **TR**: Turkey stock market (Borsa Istanbul)

## Error Handling

```python
from laplace import LaplaceClient, LaplaceAPIError

client = LaplaceClient(api_key="your-api-key")

try:
    stock = client.stocks.get_detail_by_symbol(symbol="INVALID", region="us")
except LaplaceAPIError as e:
    print(f"API Error: {e}")
    print(f"Status Code: {e.status_code}")
    print(f"Response: {e.response}")
```

## Authentication

Get your API key from the Laplace platform and initialize the client:

```python
client = LaplaceClient(api_key="your-api-key-here")
```

## Development

### Setup

```bash
git clone https://github.com/Laplace-Analytics/laplace-python-sdk.git
cd laplace-python-sdk
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=laplace

# Run integration tests (requires API key)
LAPLACE_API_KEY=your-key pytest -m integration
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0
- pydantic >= 2.0.0

## Documentation

Full API documentation is available at [laplace.finfree.co/en/docs](https://laplace.finfree.co/en/docs)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.