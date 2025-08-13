# 🛩️ Flight Data Scraper

A comprehensive Python-based flight data scraper that provides legal and ethical access to real-time flight information using multiple data sources.

## ⚠️ Important Legal Notice

**This project prioritizes legal and ethical data access:**

- ✅ **OpenSky Network API**: Free, legal, open-source flight data
- ✅ **Flightradar24 Official API**: Paid subscription required, fully legal
- ⚠️ **Web Scraping**: Educational examples only - direct scraping may violate Terms of Service

**Always use official APIs for production applications.**

## 🌟 Features

- **Multiple Data Sources**: OpenSky Network, Flightradar24 API, educational examples
- **Real-time Data**: Live flight tracking and aircraft positions
- **Geographic Filtering**: Filter flights by regions or custom bounding boxes
- **Data Export**: Export to JSON and CSV formats
- **Comprehensive Coverage**: Global flight data with detailed aircraft information
- **Rate Limiting**: Built-in respect for API rate limits
- **Educational Examples**: Learn web scraping concepts safely

## 📦 Installation

1. **Clone or download the project**:
```bash
cd /workspace
```

2. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables** (optional but recommended):
```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🚀 Quick Start

### Basic Usage

```python
from flight_scraper import FlightScraper

# Initialize the scraper
scraper = FlightScraper()

# Get current flights worldwide
flights = scraper.get_all_flights(use_opensky=True)

# Display results
print(f"Found {len(flights)} active flights")
for flight in flights[:5]:  # Show first 5
    print(f"{flight.callsign} - {flight.origin_country}")

# Export data
scraper.export_data(flights, 'json', 'flights.json')
scraper.export_data(flights, 'csv', 'flights.csv')
```

### Regional Flight Data

```python
# Get flights by region
europe_flights = scraper.get_flights_by_region('europe')
usa_flights = scraper.get_flights_by_region('usa')
asia_flights = scraper.get_flights_by_region('asia')

print(f"Europe: {len(europe_flights)} flights")
print(f"USA: {len(usa_flights)} flights")
print(f"Asia: {len(asia_flights)} flights")
```

### Custom Geographic Area

```python
from flight_scraper import OpenSkyNetworkScraper

opensky = OpenSkyNetworkScraper()

# Define custom bounding box (around New York)
ny_flights = opensky.get_flights_by_bbox(
    min_lat=40.0, min_lon=-75.0,  # Southwest corner
    max_lat=41.5, max_lon=-73.0   # Northeast corner
)

print(f"Found {len(ny_flights)} flights around New York")
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file from `.env.example`:

```bash
# OpenSky Network (optional - higher rate limits with account)
OPENSKY_USERNAME=your_username
OPENSKY_PASSWORD=your_password

# Flightradar24 API (requires subscription)
FR24_API_KEY=your_api_key

# Rate limiting
REQUEST_DELAY=1
MAX_RETRIES=3
```

### OpenSky Network Setup

1. **Free Usage**: No registration required, but limited to 1000 requests per day
2. **Registered Account**: 
   - Register at [OpenSky Network](https://opensky-network.org/)
   - Higher rate limits and additional features
   - Free for research and non-commercial use

### Flightradar24 API Setup

1. **Subscription Required**: Visit [Flightradar24 Commercial Services](https://www.flightradar24.com/commercial-services/api)
2. **Generate API Key**: Access key management after subscription
3. **Documentation**: Full API documentation available to subscribers

## 📊 Data Format

### FlightData Object

Each flight contains the following information:

```python
@dataclass
class FlightData:
    icao24: str              # Unique aircraft identifier
    callsign: str           # Flight callsign (e.g., "UAL123")
    origin_country: str     # Country of aircraft registration
    time_position: int      # Unix timestamp of position
    last_contact: int       # Last contact with aircraft
    longitude: float        # Aircraft longitude
    latitude: float         # Aircraft latitude
    baro_altitude: float    # Barometric altitude (meters)
    on_ground: bool         # Whether aircraft is on ground
    velocity: float         # Ground speed (m/s)
    true_track: float       # Aircraft heading (degrees)
    vertical_rate: float    # Climb/descent rate (m/s)
    geo_altitude: float     # Geometric altitude (meters)
    squawk: str            # Transponder squawk code
    spi: bool              # Special purpose indicator
    position_source: int   # Source of position data
```

### Export Formats

**JSON Format:**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "count": 1250,
  "flights": [
    {
      "icao24": "a12345",
      "callsign": "UAL123",
      "origin_country": "United States",
      "latitude": 40.7128,
      "longitude": -74.0060,
      "baro_altitude": 10000.0,
      "on_ground": false,
      "velocity": 250.5
    }
  ]
}
```

**CSV Format:**
```csv
icao24,callsign,origin_country,latitude,longitude,baro_altitude,on_ground,velocity
a12345,UAL123,United States,40.7128,-74.0060,10000.0,False,250.5
```

## 🎯 Usage Examples

Run the comprehensive examples:

```bash
python example_usage.py
```

This will demonstrate:
1. Basic flight data retrieval
2. Regional flight filtering
3. Specific aircraft tracking
4. Custom geographic areas
5. Basic data analysis

## 📝 API Documentation

### FlightScraper Class

The main interface for flight data access.

#### Methods

- `get_all_flights(use_opensky=True, use_fr24_api=False)` - Get global flight data
- `get_flights_by_region(region)` - Get flights for predefined regions
- `export_data(flights, format_type, filename)` - Export flight data

### OpenSkyNetworkScraper Class

Direct interface to OpenSky Network API.

#### Methods

- `get_states(icao24=None, time=None)` - Get aircraft states
- `get_flights_by_bbox(min_lat, min_lon, max_lat, max_lon)` - Geographic filtering

### Supported Regions

- `'europe'`: European airspace
- `'usa'`: United States airspace  
- `'asia'`: Asian airspace

## 🔄 Rate Limiting

The scraper implements responsible rate limiting:

- **OpenSky Network**: 1-second delays between requests
- **Automatic Retries**: Up to 3 attempts for failed requests
- **Error Handling**: Graceful handling of API errors
- **Respect ToS**: Built-in compliance with service terms

## 🛡️ Legal Compliance

### ✅ Recommended Data Sources

1. **OpenSky Network**
   - Free and legal for research
   - Open-source initiative
   - Real-time and historical data
   - No terms violations

2. **Flightradar24 Official API**
   - Paid service with official support
   - High-quality, reliable data
   - Commercial licensing available
   - Full legal compliance

### ⚠️ Web Scraping Considerations

- **Educational Purpose Only**: Web scraping examples are for learning
- **Terms of Service**: Direct scraping may violate website ToS
- **Legal Risk**: Potential account termination or legal action
- **Alternative Recommended**: Always prefer official APIs

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-feature`
3. **Commit changes**: `git commit -am 'Add new feature'`
4. **Push to branch**: `git push origin feature/new-feature`
5. **Submit pull request**

### Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include error handling
- Respect API rate limits
- Add appropriate tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**No data returned:**
- Check internet connection
- Verify API credentials (if using authenticated access)
- Ensure API rate limits aren't exceeded

**Rate limiting errors:**
- Increase delays between requests
- Register for OpenSky Network account
- Consider upgrading to paid FR24 API

**Missing dependencies:**
- Run `pip install -r requirements.txt`
- Ensure Python 3.7+ is installed

### Getting Help

1. **Check Documentation**: Review this README and code comments
2. **Review Examples**: Run `example_usage.py` for working examples
3. **API Documentation**: 
   - [OpenSky Network API](https://opensky-network.org/apidoc/)
   - [Flightradar24 API](https://www.flightradar24.com/commercial-services/api)

## 🔗 Related Resources

- [OpenSky Network](https://opensky-network.org/) - Free flight data
- [Flightradar24 API](https://www.flightradar24.com/commercial-services/api) - Commercial API
- [ICAO Aircraft Database](https://www.icao.int/) - Aircraft registration info
- [ADS-B Exchange](https://www.adsbexchange.com/) - Alternative flight tracking

---

**⚡ Quick Commands:**

```bash
# Run basic scraper
python flight_scraper.py

# Run all examples  
python example_usage.py

# Test OpenSky connection
python -c "from flight_scraper import OpenSkyNetworkScraper; s=OpenSkyNetworkScraper(); print(len(s.get_states()))"
```

**📈 Example Output:**
```
🛩️  FLIGHT DATA SCRAPER
============================================================

ℹ Using OpenSky Network without authentication (limited requests)
⚠ Flightradar24 API key not provided. Set FR24_API_KEY environment variable.
⚠ Educational scraper initialized - Use responsibly and respect ToS

📋 Example 1: Getting global flight data...

📡 Fetching from OpenSky Network...
✓ Retrieved 1247 flight records

✓ Retrieved 1247 flights

📊 Sample flight data:
1. UAL1234 (a12345) - United States
   Position: 40.7128, -74.0060
   Altitude: 10000 m
2. BAW456 (b67890) - United Kingdom  
   Position: 51.4700, -0.4543
   Altitude: 11500 m
3. DLH789 (c11111) - Germany
   Position: 52.3200, 13.4050
   Altitude: 9800 m

💾 Exporting data...
✓ Exported 1247 flights to flights_20240115_103045.json
✓ Exported 1247 flights to flights_20240115_103045.csv
```
