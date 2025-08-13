# Turkish Airlines Fleet Analyzer

A comprehensive Python tool to analyze the entire Turkish Airlines fleet using the FlightRadar24 API. This enhanced version fetches data for **ALL aircraft types** and provides detailed statistics per aircraft registration including total flight time and flight count.

## 🚀 Key Features

- ✈️ **Complete Fleet Analysis**: Fetches ALL Turkish Airlines aircraft (not just A321neo)
- 📊 **Detailed Per-Aircraft Statistics**: Registration, type, flight count, total flight hours
- 📈 **Comprehensive Analytics**: Flight patterns, route analysis, utilization metrics
- 📅 **Flexible Time Periods**: Analyze any time range (e.g., past 365 days)
- 💾 **Multiple Export Formats**: CSV and JSON exports for further analysis
- 🔍 **Aircraft Type Breakdown**: Statistics grouped by aircraft type
- 🏆 **Top Performers**: Rankings by flight count and flight hours
- 📋 **Route Analysis**: Most common routes per aircraft

## 📋 What You Get

### Per-Aircraft Statistics:
- **Registration Number** (e.g., TC-LTI, TC-JOY)
- **Aircraft Type** (e.g., A21N, B77W, A333, B38M)
- **Total Flight Count** in the specified period
- **Total Flight Time** (hours and minutes)
- **Average Flight Duration** per flight
- **Unique Routes** flown
- **Most Common Route** and frequency
- **Date Range** of operations

### Fleet-Wide Analytics:
- Complete aircraft type breakdown
- Top performers by flight count
- Top performers by flight hours
- Fleet utilization statistics
- Route popularity analysis

## 📦 Installation

1. **Download the files:**
   ```bash
   # Main files needed:
   # - turkish_airlines_fleet_analyzer.py
   # - requirements.txt
   # - quick_example.py (for testing)
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🔑 Setup

### API Key Configuration

Set your FlightRadar24 API key using either method:

#### Method 1: Environment Variable (Recommended)
```bash
export FLIGHTRADAR24_API_KEY="your_api_key_here"
```

#### Method 2: Direct Input
The script will prompt you to enter your API key if not set as environment variable.

## 🖥️ Usage

### Basic Usage (Full Analysis)

For a complete fleet analysis (default: 365 days):

```bash
python turkish_airlines_fleet_analyzer.py
```

### Quick Testing (7 days)

For faster testing with a smaller dataset:

```bash
python quick_example.py
```

### Interactive Options

The main script will ask:
1. **API Key** (if not set as environment variable)
2. **Time Period** (default: 365 days)

Example:
```
Enter number of days to look back (default 365): 180
```

## 📊 Output Examples

### Console Output Sample
```
Found 387 aircraft in Turkish Airlines fleet
Aircraft types in fleet:
  A21N: 57 aircraft
  A333: 15 aircraft
  A339: 23 aircraft
  A359: 9 aircraft
  B38M: 85 aircraft
  B77W: 25 aircraft
  B789: 35 aircraft
  ...

================================================================================
TURKISH AIRLINES FLEET ANALYSIS - DETAILED SUMMARY
================================================================================
Total Aircraft in Fleet: 387
Active Aircraft (with flights): 342
Total Flights: 45,678
Total Flight Hours: 234,567.5
Average Flight Hours per Aircraft: 686.2

                            AIRCRAFT TYPE SUMMARY
--------------------------------------------------------------------------------
Type     Count  Flights  Hours      Avg Hours/Aircraft
--------------------------------------------------------------------------------
A21N     57     12,456   45,678.2   801.4
B38M     85     15,789   52,345.7   615.8
B77W     25     3,456    28,976.4   1,159.1
...

                            TOP PERFORMING AIRCRAFT
--------------------------------------------------------------------------------

Top 10 by Flight Count:
Registration Type     Flights  Hours      Avg/Flight
TC-JOY       B38M     245      789.5      3.2
TC-LTI       A21N     238      756.8      3.2
...

Top 10 by Flight Hours:
Registration Type     Hours      Flights  Routes
TC-JMK       B77W     1,456.2    89       67
TC-LLA       A339     1,234.8    134      45
...

                        DETAILED AIRCRAFT BREAKDOWN
--------------------------------------------------------------------------------
Registration Type     Flights  Hours      Routes  Top Route
TC-AAA       A21N     156      487.3      23      IST-ESB
TC-BBB       B38M     189      623.7      34      IST-ADB
...
```

### CSV Output Structure

#### Aircraft Statistics CSV (`turkish_airlines_aircraft_stats.csv`):
```csv
registration,aircraft_type,total_flights,total_flight_time_hours,total_flight_time_minutes,average_flight_time_minutes,first_flight_date,last_flight_date,unique_routes,most_common_route,most_common_route_count
TC-LTI,A21N,238,756.8,45408,190.8,2024-01-15,2024-12-31,34,IST-ESB,45
TC-JOY,B38M,245,789.5,47370,193.3,2024-01-12,2024-12-30,28,IST-ADB,52
```

#### All Flights CSV (`turkish_airlines_all_flights.csv`):
```csv
registration,aircraft_type,flight_number,departure_airport,arrival_airport,departure_time,arrival_time,flight_duration,duration_minutes,status,date
TC-LTI,A21N,TK2233,IST,ESB,2024-01-15 08:30:00,2024-01-15 09:45:00,01:15,75,Landed,2024-01-15
TC-LTI,A21N,TK2234,ESB,IST,2024-01-15 10:30:00,2024-01-15 11:45:00,01:15,75,Landed,2024-01-15
```

## 📁 Generated Files

### Main Analysis Files:
1. **`turkish_airlines_aircraft_stats.csv`** - Per-aircraft statistics summary
2. **`turkish_airlines_all_flights.csv`** - Individual flight records
3. **`aircraft_stats.json`** - Statistics in JSON format
4. **`all_flights.json`** - Flight records in JSON format

### Sample/Test Files (from quick_example.py):
1. **`sample_aircraft_stats.csv`** - Sample statistics
2. **`sample_all_flights.csv`** - Sample flight data

## 🔍 Data Analysis Capabilities

### Fleet Utilization Analysis
```python
from turkish_airlines_fleet_analyzer import TurkishAirlinesFleetAnalyzer

analyzer = TurkishAirlinesFleetAnalyzer(api_key)
stats = analyzer.analyze_fleet(days_back=365)

# Find most utilized aircraft
most_active = max(stats.values(), key=lambda x: x.total_flights)
print(f"Most active: {most_active.registration} with {most_active.total_flights} flights")

# Calculate fleet average utilization
total_hours = sum(s.total_flight_time_hours for s in stats.values())
active_aircraft = len([s for s in stats.values() if s.total_flights > 0])
avg_utilization = total_hours / active_aircraft
print(f"Average utilization: {avg_utilization:.1f} hours per aircraft")
```

### Aircraft Type Comparison
```python
# Group by aircraft type
from collections import defaultdict

type_stats = defaultdict(lambda: {'aircraft': 0, 'flights': 0, 'hours': 0})
for stats in aircraft_stats.values():
    type_stats[stats.aircraft_type]['aircraft'] += 1
    type_stats[stats.aircraft_type]['flights'] += stats.total_flights
    type_stats[stats.aircraft_type]['hours'] += stats.total_flight_time_hours

for aircraft_type, data in type_stats.items():
    avg_flights = data['flights'] / data['aircraft']
    avg_hours = data['hours'] / data['aircraft']
    print(f"{aircraft_type}: {avg_flights:.1f} avg flights, {avg_hours:.1f} avg hours per aircraft")
```

### Route Analysis
```python
# Find most popular routes across fleet
from collections import Counter

all_routes = []
for flight in analyzer.all_flights:
    if flight.departure_airport and flight.arrival_airport:
        all_routes.append(f"{flight.departure_airport}-{flight.arrival_airport}")

top_routes = Counter(all_routes).most_common(10)
print("Top 10 routes:")
for route, count in top_routes:
    print(f"  {route}: {count} flights")
```

## ⚙️ Script Customization

### Change Time Period
```python
# Analyze last 180 days instead of 365
analyzer.analyze_fleet(days_back=180)
```

### Filter by Aircraft Type
```python
# Get only A321neo aircraft stats
a21n_aircraft = {reg: stats for reg, stats in aircraft_stats.items() 
                 if stats.aircraft_type == "A21N"}
```

### Change Airline
To analyze a different airline, modify the airline code:
```python
fleet = self.api.get_airline_fleet("LH")  # Lufthansa
```

## 🔧 Advanced Features

### Performance Monitoring
- **Rate Limiting**: Built-in 1-second delays between API calls
- **Error Handling**: Robust error handling for API failures
- **Progress Tracking**: Real-time progress updates during analysis
- **Memory Efficient**: Processes aircraft one at a time

### Data Validation
- **Duration Calculation**: Accurate flight time calculations
- **Date Parsing**: Proper timestamp handling
- **Missing Data**: Graceful handling of incomplete records

## ⚠️ Important Notes

1. **API Limits**: The script respects FlightRadar24 API rate limits
2. **Processing Time**: Full fleet analysis can take 30-60 minutes
3. **Data Accuracy**: Results depend on FlightRadar24's data completeness
4. **Subscription Required**: Requires valid FlightRadar24 API subscription

## 🚀 Performance Tips

1. **Start Small**: Use `quick_example.py` for initial testing
2. **Incremental Analysis**: Analyze shorter time periods first
3. **Monitor Progress**: Watch console output for progress updates
4. **Check Exports**: Verify CSV files are being created correctly

## 🔧 Troubleshooting

### Common Issues

1. **"No aircraft found"**
   - Verify API key is correct
   - Check FlightRadar24 subscription status
   - Ensure internet connectivity

2. **Slow Processing**
   - Normal for large fleets (387+ aircraft)
   - Consider shorter time periods for faster results
   - Check API rate limiting

3. **Incomplete Data**
   - Some aircraft may have limited flight history
   - Historical data availability varies by subscription tier

### Testing API Connection
```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.flightradar24.com/common/v1/airline/fleet.json?airline=TK"
```

## 📊 Sample Analysis Results

Based on a typical analysis, you might expect:

- **Total Aircraft**: 387 aircraft across multiple types
- **Active Aircraft**: ~350 aircraft with recent flights
- **Flight Data**: 40,000+ flights for a 365-day period
- **Aircraft Types**: A21N, B38M, B77W, A333, A339, B789, etc.
- **Processing Time**: 20-45 minutes for full fleet analysis

## 📄 License

This tool is for educational and research purposes. Ensure compliance with FlightRadar24's terms of service and API usage policies.

---

**💡 Pro Tip**: Start with `quick_example.py` using a 7-day period to verify your setup before running the full 365-day analysis!