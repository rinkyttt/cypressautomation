# 🆓 Free Flight Data Scraper Guide

**Zero cost, zero API keys, zero registration required!**

## 🚀 Quick Start (30 seconds)

```bash
# 1. Run the free scraper
python free_flight_scraper.py

# 2. That's it! Your data will be saved automatically
```

## 📊 What You Get (FREE)

- ✅ **Real-time flight data** from around the world
- ✅ **1000 API requests per day** (no registration)
- ✅ **4000 requests/day** with free OpenSky account
- ✅ **JSON and CSV exports** automatically generated
- ✅ **Geographic filtering** by custom areas
- ✅ **Flight statistics** and analysis
- ✅ **Completely legal** and ethical data source

## 🎯 Simple Examples

### Example 1: Get All Flights Worldwide

```python
from free_flight_scraper import FreeFlightScraper

# Initialize (no API key needed!)
scraper = FreeFlightScraper()

# Get all flights
flights = scraper.get_all_flights()

# Export data
scraper.export_to_json(flights)
scraper.export_to_csv(flights)
```

### Example 2: Get Flights in Specific Area

```python
# Get flights around New York
ny_flights = scraper.get_flights_in_area(
    min_lat=40.0, min_lon=-75.0,  # Southwest corner
    max_lat=41.5, max_lon=-73.0   # Northeast corner
)

print(f"Found {len(ny_flights)} flights around NYC")
```

### Example 3: Popular Regions

```python
# Get flights from major regions (uses 3 requests)
regional_data = scraper.get_popular_regions()

for region, flights in regional_data.items():
    print(f"{region}: {len(flights)} flights")
```

## 🌍 Coordinate Examples

**Major Cities:**
```python
# London, UK
london_flights = scraper.get_flights_in_area(51.0, -1.0, 52.0, 1.0)

# Tokyo, Japan  
tokyo_flights = scraper.get_flights_in_area(35.0, 139.0, 36.0, 140.5)

# Los Angeles, USA
la_flights = scraper.get_flights_in_area(33.5, -119.0, 34.5, -117.5)

# Sydney, Australia
sydney_flights = scraper.get_flights_in_area(-34.5, 150.5, -33.5, 151.5)
```

## 📈 Maximize Your Free Usage

### Anonymous Usage (1000 requests/day)
- Perfect for occasional use
- No registration required
- About 1 month of daily worldwide snapshots

### Free Account (4000 requests/day)  
- 4x more requests per day
- Still completely free
- Register at [OpenSky Network](https://opensky-network.org/)

```python
# Use with free account
scraper = FreeFlightScraper(
    use_account=True,
    username="your_username", 
    password="your_password"
)
```

## ⚡ Rate Limiting (Built-in)

The scraper automatically:
- ✅ Waits 6+ seconds between requests
- ✅ Tracks your daily usage  
- ✅ Shows remaining requests
- ✅ Respects API limits

## 📁 Output Files

**JSON Format (structured data):**
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "source": "OpenSky Network (Free API)", 
  "count": 1247,
  "flights": [
    {
      "icao24": "a12345",
      "callsign": "UAL123",
      "country": "United States",
      "position": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "altitude_m": 10000
      },
      "on_ground": false,
      "velocity_ms": 250.5
    }
  ]
}
```

**CSV Format (spreadsheet-friendly):**
```csv
icao24,callsign,country,latitude,longitude,altitude_m,on_ground,velocity_ms
a12345,UAL123,United States,40.7128,-74.0060,10000,False,250.5
```

## 🔥 Quick Commands

```bash
# Test connection
python -c "from free_flight_scraper import FreeFlightScraper; s=FreeFlightScraper(); print(f'✅ Found {len(s.get_all_flights())} flights')"

# Get only European flights
python -c "from free_flight_scraper import FreeFlightScraper; s=FreeFlightScraper(); flights=s.get_flights_in_area(35,-25,70,40); s.export_to_json(flights, 'europe.json')"

# Show statistics only
python -c "from free_flight_scraper import FreeFlightScraper; s=FreeFlightScraper(); flights=s.get_all_flights(); s.show_statistics(flights)"
```

## 🎨 Sample Output

```
🛩️  FREE FLIGHT DATA SCRAPER
═══════════════════════════════════════════

ℹ️  Using OpenSky Network anonymously
📊 Daily limit: 1000 requests (no registration needed)
🌐 Data source: OpenSky Network (Free & Legal)
⚡ Rate limit: ~10 requests per minute

📡 Request #1/1000

🌍 Fetching worldwide flight data...
✅ Retrieved 11,247 flights

✈️  SAMPLE FLIGHTS:
1. UAL1234 (a12345)
   Country: United States
   Status: ✈️  Airborne
   Position: 40.7128, -74.0060
   Altitude: 10000m (32808ft)

📊 FLIGHT STATISTICS
═══════════════════
Total aircraft: 11,247
✈️  Airborne: 8,156
🛬 On ground: 3,091

🌍 TOP COUNTRIES:
   United States: 2,847 (25.3%)
   Germany: 892 (7.9%)
   United Kingdom: 743 (6.6%)

💾 Exported 11,247 flights to flights_free_20240115_103045.json
📝 Exported 11,247 flights to flights_free_20240115_103045.csv
```

## ❓ FAQ

**Q: Is this really free?**
A: Yes! OpenSky Network is a non-profit providing free flight data.

**Q: Do I need to register?**
A: No, but registering gives you 4x more requests (still free).

**Q: Is this legal?**
A: Absolutely! OpenSky Network provides this data legally and openly.

**Q: How accurate is the data?**
A: Very accurate - it's real ADS-B data from aircraft transponders.

**Q: Can I use this commercially?**
A: For research/personal use, yes. For commercial use, check OpenSky's terms.

**Q: What happens if I exceed the limit?**
A: You'll get rate limited until midnight UTC (resets daily).

## 🌟 Pro Tips

1. **Run once daily** to get a complete snapshot
2. **Use geographic filtering** to focus on areas of interest  
3. **Register for free account** to get 4x more requests
4. **Monitor your usage** - the scraper shows remaining requests
5. **Export immediately** - data is live and changes constantly

---

**🎯 Ready to start? Just run:**
```bash
python free_flight_scraper.py
```

**No setup, no API keys, no payment required!** 🚀