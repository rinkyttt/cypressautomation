# 🛩️ Flightradar24 Official API Client Documentation

**Complete guide to using the FR24 API for professional flight tracking**

## 🚀 Quick Start

### 1. Prerequisites
- Flightradar24 API subscription
- Python 3.8+
- Required packages: `requests`, `python-dotenv`

### 2. Installation
```bash
# Install dependencies
pip install requests python-dotenv

# Download the client files
# - flightradar24_api_client.py
# - fr24_examples.py
```

### 3. Setup
```bash
# Set your API token
export FR24_API_TOKEN=your_api_token_here

# Or create .env file
echo "FR24_API_TOKEN=your_api_token_here" > .env
```

### 4. Basic Usage
```python
from flightradar24_api_client import FlightRadar24Client

# Initialize client
client = FlightRadar24Client()

# Get live flights
flights = client.get_live_flights()
print(f"Found {len(flights)} flights")

# Export data
client.export_to_json(flights, "my_flights.json")
```

## 📚 API Reference

### FlightRadar24Client Class

#### Constructor
```python
client = FlightRadar24Client(api_token=None)
```
- `api_token`: Your FR24 API token (optional if using environment variable)

#### Core Methods

##### Live Flight Data
```python
# Get live flights worldwide
flights = client.get_live_flights()

# Get flights in geographic bounds
ny_bounds = {'north': 41.0, 'south': 40.0, 'east': -73.0, 'west': -75.0}
flights = client.get_live_flights(bounds=ny_bounds)

# Filter by aircraft type
flights = client.get_live_flights(aircraft_type='B738')
```

##### Flight Details
```python
# Get detailed flight information
details = client.get_flight_details(flight_id)

# Get flight track (historical positions)
track = client.get_flight_track(flight_id)

# Get historical playback data
playback = client.get_playback_data(flight_id, timestamp)
```

##### Airport Information
```python
# Get airport info
airport_info = client.get_airport_info('JFK')

# Get arrivals
arrivals = client.get_airport_arrivals('JFK', limit=100)

# Get departures
departures = client.get_airport_departures('JFK', limit=100)
```

##### Airline Information
```python
# Get airline info
airline_info = client.get_airline_info('AA')

# Get airline fleet
fleet = client.get_airline_fleet('AA')
```

##### Search and Lookup
```python
# Search flights
results = client.search_flights('AA100', limit=50)

# Get aircraft info
aircraft_info = client.get_aircraft_info('N12345')
```

##### Data Export
```python
# Export to JSON
client.export_to_json(data, 'filename.json')

# Export flights to CSV
client.export_flights_to_csv(flights, 'flights.csv')

# Generate statistics
stats = client.get_statistics(flights)
```

##### Utility Methods
```python
# Test API connection
if client.test_connection():
    print("API connection successful")
```

### FR24DataCollector Class

High-level data collection interface:

```python
from flightradar24_api_client import FR24DataCollector

collector = FR24DataCollector()

# Collect comprehensive airport data
airport_data = collector.collect_airport_data('JFK')

# Collect airline data
airline_data = collector.collect_airline_data('AA')

# Collect regional flight data
bounds = {'north': 41.0, 'south': 40.0, 'east': -73.0, 'west': -75.0}
region_data = collector.collect_region_flights(bounds, "New York Area")
```

## 🎯 Usage Examples

### Example 1: Monitor Airport Operations
```python
from flightradar24_api_client import FlightRadar24Client

client = FlightRadar24Client()

# Get JFK operations
arrivals = client.get_airport_arrivals('JFK')
departures = client.get_airport_departures('JFK')

print(f"JFK: {len(arrivals)} arrivals, {len(departures)} departures")

# Find busiest routes
routes = {}
for flight in departures:
    dest = flight.get('destination', {}).get('iata', 'Unknown')
    routes[dest] = routes.get(dest, 0) + 1

top_routes = sorted(routes.items(), key=lambda x: x[1], reverse=True)[:5]
print("Top destinations:", top_routes)
```

### Example 2: Track Specific Flight
```python
# Search for a specific flight
results = client.search_flights('AA100')

if results:
    flight_id = results[0].get('id')
    
    # Get detailed information
    details = client.get_flight_details(flight_id)
    track = client.get_flight_track(flight_id)
    
    print(f"Flight: {details.get('callsign')}")
    print(f"Route: {details.get('origin', {}).get('iata')} → {details.get('destination', {}).get('iata')}")
    print(f"Track points: {len(track.get('data', []))}")
```

### Example 3: Analyze Regional Traffic
```python
# Define region (e.g., Europe)
europe_bounds = {
    'north': 70.0, 'south': 35.0,
    'east': 40.0, 'west': -25.0
}

# Get flights in region
flights = client.get_live_flights(bounds=europe_bounds)

# Generate statistics
stats = client.get_statistics(flights)

print(f"European flights: {stats['total_flights']}")
print("Top airlines:", list(stats['airlines'].items())[:5])
print("Top aircraft:", list(stats['aircraft_types'].items())[:5])

# Export data
client.export_to_json(flights, "europe_flights.json")
client.export_flights_to_csv(flights, "europe_flights.csv")
```

### Example 4: Airline Fleet Analysis
```python
# Analyze airline fleet
airline_info = client.get_airline_info('AA')
fleet = client.get_airline_fleet('AA')

print(f"Airline: {airline_info.get('name')}")
print(f"Fleet size: {len(fleet)}")

# Analyze aircraft types
aircraft_types = {}
for aircraft in fleet:
    model = aircraft.get('aircraft', {}).get('model', 'Unknown')
    aircraft_types[model] = aircraft_types.get(model, 0) + 1

print("Fleet composition:")
for aircraft_type, count in sorted(aircraft_types.items(), key=lambda x: x[1], reverse=True):
    print(f"  {aircraft_type}: {count} aircraft")
```

## 📊 Data Structures

### Flight Data
```python
{
    "id": "flight_identifier",
    "callsign": "AA100",
    "origin": {
        "iata": "JFK",
        "icao": "KJFK",
        "name": "John F. Kennedy International Airport"
    },
    "destination": {
        "iata": "LAX",
        "icao": "KLAX", 
        "name": "Los Angeles International Airport"
    },
    "aircraft": {
        "model": "Boeing 737-800",
        "registration": "N12345"
    },
    "status": "en-route",
    "departure_time": "2024-01-15T10:30:00Z",
    "arrival_time": "2024-01-15T14:45:00Z",
    "position": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "altitude": 35000,
        "speed": 450,
        "heading": 270
    }
}
```

### Airport Data
```python
{
    "iata": "JFK",
    "icao": "KJFK",
    "name": "John F. Kennedy International Airport",
    "city": "New York",
    "country": "United States",
    "timezone": "America/New_York",
    "coordinates": {
        "latitude": 40.6413,
        "longitude": -73.7781
    }
}
```

### Airline Data
```python
{
    "iata": "AA",
    "icao": "AAL",
    "name": "American Airlines",
    "country": "United States",
    "website": "https://www.aa.com"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
FR24_API_TOKEN=your_api_token_here

# Optional
FR24_BASE_URL=https://fr24api.flightradar24.com/v1  # Custom base URL
FR24_TIMEOUT=30                                      # Request timeout in seconds
FR24_RATE_LIMIT=0.1                                 # Min seconds between requests
```

### Rate Limiting
The client implements automatic rate limiting:
- Default: 100ms between requests
- Respects API rate limits
- Automatic retry on rate limit errors
- Configurable timing

### Error Handling
```python
try:
    flights = client.get_live_flights()
except ValueError as e:
    print(f"Authentication error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## 📈 Best Practices

### 1. Efficient API Usage
```python
# Use geographic bounds to limit data
bounds = {'north': 45.0, 'south': 35.0, 'east': -75.0, 'west': -85.0}
flights = client.get_live_flights(bounds=bounds)

# Filter by aircraft type when needed
boeing_flights = client.get_live_flights(aircraft_type='B737')

# Use appropriate limits
arrivals = client.get_airport_arrivals('JFK', limit=50)
```

### 2. Data Management
```python
# Export data immediately after collection
flights = client.get_live_flights()
client.export_to_json(flights, f"flights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

# Use compression for large datasets
import gzip
import json

with gzip.open('flights.json.gz', 'wt') as f:
    json.dump(flights, f)
```

### 3. Monitoring and Logging
```python
import logging

# Enable detailed logging
logging.basicConfig(level=logging.INFO)

# Monitor API usage
client = FlightRadar24Client()
print(f"API requests made: {client.request_count}")
```

## 🚨 Error Handling

### Common Errors
```python
# Authentication failed
ValueError: Invalid API token

# Rate limit exceeded  
Exception: Rate limit exceeded

# Network errors
requests.exceptions.RequestException: Connection timeout

# Invalid parameters
requests.exceptions.HTTPError: 400 Bad Request
```

### Error Recovery
```python
import time
from requests.exceptions import RequestException

def robust_api_call(client, method, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return getattr(client, method)(*args, **kwargs)
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff

# Usage
flights = robust_api_call(client, 'get_live_flights', bounds=bounds)
```

## 📊 Performance Tips

### 1. Batch Operations
```python
# Collect related data in batches
airports = ['JFK', 'LAX', 'LHR', 'CDG']
airport_data = {}

for airport in airports:
    airport_data[airport] = {
        'info': client.get_airport_info(airport),
        'arrivals': client.get_airport_arrivals(airport),
        'departures': client.get_airport_departures(airport)
    }
    time.sleep(1)  # Rate limiting
```

### 2. Caching
```python
import pickle
from datetime import datetime, timedelta

class CachedFR24Client:
    def __init__(self, client):
        self.client = client
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_cached_flights(self, bounds=None):
        cache_key = str(bounds)
        now = datetime.now()
        
        if cache_key in self.cache:
            data, timestamp = self.cache[cache_key]
            if now - timestamp < self.cache_duration:
                return data
        
        # Fetch fresh data
        flights = self.client.get_live_flights(bounds=bounds)
        self.cache[cache_key] = (flights, now)
        return flights
```

## 🔗 Integration Examples

### Web Dashboard
```python
from flask import Flask, jsonify
from flightradar24_api_client import FlightRadar24Client

app = Flask(__name__)
client = FlightRadar24Client()

@app.route('/api/flights')
def get_flights():
    bounds = request.args.to_dict()
    flights = client.get_live_flights(bounds=bounds)
    return jsonify(flights)

@app.route('/api/airport/<code>')
def get_airport(code):
    data = {
        'info': client.get_airport_info(code),
        'arrivals': client.get_airport_arrivals(code),
        'departures': client.get_airport_departures(code)
    }
    return jsonify(data)
```

### Database Storage
```python
import sqlite3
import json

def store_flights_in_db(flights):
    conn = sqlite3.connect('flights.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id TEXT PRIMARY KEY,
            callsign TEXT,
            data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    for flight in flights:
        cursor.execute('''
            INSERT OR REPLACE INTO flights (id, callsign, data)
            VALUES (?, ?, ?)
        ''', (
            flight.get('id'),
            flight.get('callsign'),
            json.dumps(flight)
        ))
    
    conn.commit()
    conn.close()
```

## 📝 License & Support

- **License**: MIT License
- **Support**: Check FR24 API documentation and support channels
- **Rate Limits**: Varies by subscription plan
- **Data Usage**: Follow FR24 Terms and Conditions

## 🔧 Troubleshooting

### Common Issues

**1. Authentication Errors**
```bash
# Check your token
echo $FR24_API_TOKEN

# Verify token format (should be long alphanumeric string)
# Get new token from FR24 dashboard if needed
```

**2. No Data Returned**
```python
# Check API limits
if client.test_connection():
    print("API working, check your query parameters")
else:
    print("API connection failed")
```

**3. Rate Limiting**
```python
# Increase delays between requests
client.min_request_interval = 1.0  # 1 second

# Check your subscription limits
```

**4. Large Data Sets**
```python
# Use geographic filtering
bounds = {'north': 45, 'south': 35, 'east': -65, 'west': -85}
flights = client.get_live_flights(bounds=bounds)

# Process data in chunks
for i in range(0, len(flights), 1000):
    chunk = flights[i:i+1000]
    process_chunk(chunk)
```

---

**🎯 Ready to start? Run the examples:**
```bash
python fr24_examples.py
```

**Need help? Check:**
- FR24 API Documentation: https://support.fr24.com/
- Your FR24 dashboard for usage stats
- API status page for service updates

**Professional flight tracking made easy!** ✈️🌍