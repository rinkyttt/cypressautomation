# 🛩️ Flightradar24 Official API Setup Guide

**Get REAL Flightradar24 data legally and reliably!**

## 🚀 Quick Setup (5 minutes)

### Step 1: Subscribe to FR24 API
1. Go to: https://www.flightradar24.com/commercial-services/api
2. Choose a subscription plan
3. Complete registration and payment

### Step 2: Get Your API Key
1. Log in to your FR24 account
2. Go to "Key Management" section
3. Generate a new API token
4. Copy the token

### Step 3: Configure Environment
```bash
# Set your API key
export FR24_API_KEY=your_api_key_here

# Or create .env file
echo "FR24_API_KEY=your_api_key_here" > .env
```

### Step 4: Test Connection
```bash
python fr24_official_api.py
```

## 💰 Pricing (Check Latest on Website)

**Starter Plan** (~$50/month)
- 100,000 requests/month
- Real-time flight data
- Historical data access
- Basic support

**Professional Plan** (~$200/month)  
- 500,000 requests/month
- Advanced endpoints
- Priority support
- Custom integrations

**Enterprise Plan** (Custom)
- Unlimited requests
- Dedicated support
- Custom data feeds
- SLA guarantees

## 📊 What You Get

✅ **Real-time flight positions**
✅ **Historical flight data**
✅ **Airport information**
✅ **Flight schedules**
✅ **Aircraft details**
✅ **Weather data**
✅ **Alerts and notifications**
✅ **High-quality, reliable data**
✅ **Official support**
✅ **Legal compliance**

## 🎯 Sample Code

```python
from fr24_official_api import FlightRadar24API

# Initialize with API key
fr24 = FlightRadar24API("your_api_key")

# Get flights in area
flights = fr24.get_flights_in_bounds(
    north=41.0, south=40.0,
    east=-73.0, west=-75.0
)

# Get airport flights
jfk_flights = fr24.get_airport_flights("JFK")

# Export data
fr24.export_to_json(flights, "my_flights.json")
```

## 🔧 API Features

**Geographic Queries:**
- Flights in bounding box
- Flights near coordinates
- Regional flight data

**Airport Data:**
- Departures and arrivals
- Flight schedules
- Airport information

**Flight Details:**
- Real-time positions
- Historical tracks
- Aircraft information

**Advanced Features:**
- Flight alerts
- Custom notifications
- Data streaming

## 📚 Documentation

- **Official Docs**: https://support.fr24.com/support/solutions/articles/3000128166
- **API Reference**: Available after subscription
- **Code Samples**: Provided in developer portal
- **SDKs**: Python, JavaScript, Java available

## ✅ Benefits vs Web Scraping

| Feature | Official API | Web Scraping |
|---------|--------------|--------------|
| **Legal** | ✅ Fully legal | ❌ Violates ToS |
| **Reliable** | ✅ 99%+ uptime | ❌ Breaks easily |
| **Support** | ✅ Official help | ❌ No support |
| **Data Quality** | ✅ High quality | ❌ Inconsistent |
| **Rate Limits** | ✅ Clear limits | ❌ Risk of ban |
| **Updates** | ✅ Auto-updated | ❌ Requires maintenance |

## 🆓 Free Alternative

If you need a free option, use **OpenSky Network**:
```bash
python free_flight_scraper.py
```

## 🚨 Important Notes

- **No Web Scraping**: Direct scraping violates FR24 ToS
- **Use Official API**: Only legal way to get FR24 data
- **Check Pricing**: Plans may change
- **Read Terms**: Understand usage limits
- **Contact Support**: For custom needs

---

**🎯 Ready to start?**
1. Subscribe: https://www.flightradar24.com/commercial-services/api
2. Get API key
3. Run: `python fr24_official_api.py`

**Professional, legal, reliable flight data!** ✈️