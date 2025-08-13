# Turkish Airlines A321neo Fleet Tracker

A Python script to fetch and analyze flight data for Turkish Airlines' Airbus A321neo (A21N) fleet using the FlightRadar24 API.

## Features

- 🛫 Fetches complete Turkish Airlines A321neo fleet information
- 📊 Retrieves detailed flight history for each aircraft
- 📈 Provides comprehensive flight analytics and statistics
- 💾 Exports data to both CSV and JSON formats
- ⏱️ Calculates flight durations and route analysis
- 🔄 Rate-limited API calls to respect FlightRadar24 limits

## Prerequisites

- Python 3.7 or higher
- FlightRadar24 API subscription and API key
- Internet connection

## Installation

1. Clone or download the script files:
   ```bash
   # The main files you need:
   # - turkish_airlines_a321neo_tracker.py
   # - requirements.txt
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### API Key Setup

You have two options to provide your FlightRadar24 API key:

#### Option 1: Environment Variable (Recommended)
```bash
export FLIGHTRADAR24_API_KEY="your_api_key_here"
```

#### Option 2: Interactive Input
The script will prompt you to enter your API key if it's not set as an environment variable.

## Usage

### Basic Usage

Run the script with default settings (30 days of flight history):

```bash
python turkish_airlines_a321neo_tracker.py
```

### Interactive Options

The script will ask you:
1. **API Key** (if not set as environment variable)
2. **Days to look back** (default: 30 days)

Example interaction:
```
Enter number of days to look back (default 30): 60
```

### Output Files

The script generates two output files:

1. **`turkish_airlines_a321neo_flights.csv`** - Tabular data for spreadsheet analysis
2. **`turkish_airlines_a321neo_flights.json`** - Structured data for programmatic use

## Data Fields

Each flight record contains:

| Field | Description |
|-------|-------------|
| `registration` | Aircraft registration number (e.g., TC-LTI) |
| `flight_number` | Flight number (e.g., TK1985) |
| `departure_airport` | IATA code of departure airport |
| `arrival_airport` | IATA code of arrival airport |
| `departure_time` | Scheduled departure time (YYYY-MM-DD HH:MM:SS) |
| `arrival_time` | Scheduled arrival time (YYYY-MM-DD HH:MM:SS) |
| `flight_duration` | Flight duration (HH:MM format) |
| `aircraft_type` | Aircraft type code (A21N) |
| `status` | Flight status |
| `date` | Flight date (YYYY-MM-DD) |

## Example Output

### Console Output
```
Fetching Turkish Airlines A321neo fleet information...
Found 57 A321neo aircraft in Turkish Airlines fleet
Processing aircraft 1/57: TC-LTI
Retrieved 24 flights for aircraft TC-LTI
Processing aircraft 2/57: TC-LTF
Retrieved 28 flights for aircraft TC-LTF
...
Total flights retrieved: 1,342

============================================================
TURKISH AIRLINES A321NEO FLEET SUMMARY
============================================================
Total Aircraft: 57
Total Flights: 1,342

Flights per Aircraft:
  TC-LTA: 23 flights, Avg Duration: 2.3 hours
  TC-LTB: 26 flights, Avg Duration: 2.1 hours
  ...

Top 10 Routes:
  IST-ESB: 89 flights
  ESB-IST: 87 flights
  IST-ADB: 76 flights
  ...
```

### CSV Sample
```csv
registration,flight_number,departure_airport,arrival_airport,departure_time,arrival_time,flight_duration,aircraft_type,status,date
TC-LTI,TK2233,IST,ESB,2024-01-15 08:30:00,2024-01-15 09:45:00,01:15,A21N,Landed,2024-01-15
TC-LTI,TK2234,ESB,IST,2024-01-15 10:30:00,2024-01-15 11:45:00,01:15,A21N,Landed,2024-01-15
```

## API Endpoints Used

The script uses these FlightRadar24 API endpoints:

1. **Fleet Information**: `GET /common/v1/airline/fleet.json?airline=TK`
2. **Flight History**: `GET /common/v1/flight/list.json?registration={reg}&from={timestamp}&to={timestamp}`

## Rate Limiting

The script includes built-in rate limiting:
- 1-second delay between aircraft requests
- Proper error handling for API failures
- Retry logic for temporary failures

## Troubleshooting

### Common Issues

1. **"API key is required"**
   - Ensure you've set the `FLIGHTRADAR24_API_KEY` environment variable
   - Or enter it when prompted by the script

2. **"No A321neo aircraft found"**
   - Check your API key validity
   - Verify your FlightRadar24 subscription includes fleet data access

3. **"Error fetching fleet data"**
   - Check your internet connection
   - Verify API key is correct
   - Ensure your API subscription is active

4. **Rate limiting errors**
   - The script includes delays, but if you encounter issues, you can modify the `time.sleep(1)` value in the code

### API Key Validation

To test if your API key works:
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.flightradar24.com/common/v1/airline/fleet.json?airline=TK"
```

## Data Analysis Ideas

With the exported data, you can analyze:

- **Fleet Utilization**: Average flights per aircraft per day
- **Route Patterns**: Most popular routes and frequencies
- **Operational Efficiency**: Average flight durations vs. scheduled times
- **Seasonal Trends**: Flight patterns over different time periods
- **Hub Analysis**: Primary departure/arrival airports

## Script Customization

### Modify Aircraft Type Filter

To track different aircraft types, modify line 58 in the script:
```python
if aircraft.get("type", "").upper() == "A21N"  # Change A21N to desired type
```

### Change Airline

To track a different airline, modify the airline code:
```python
fleet = self.api.get_airline_fleet("TK")  # Change TK to desired airline
```

### Adjust Time Range

Modify the default days_back parameter:
```python
def fetch_fleet_data(self, days_back: int = 60)  # Change 30 to desired days
```

## License

This script is provided as-is for educational and research purposes. Please ensure compliance with FlightRadar24's terms of service and API usage policies.

## Support

For issues related to:
- **FlightRadar24 API**: Contact FlightRadar24 support
- **Script functionality**: Check the troubleshooting section above
- **Data accuracy**: Verify against FlightRadar24 website

---

**Note**: This tool requires a valid FlightRadar24 API subscription. Flight data accuracy depends on FlightRadar24's data sources and may have limitations based on your subscription tier.