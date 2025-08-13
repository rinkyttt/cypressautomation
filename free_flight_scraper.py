#!/usr/bin/env python3
"""
Free Flight Data Scraper - OpenSky Network
==========================================

A simplified flight data scraper using the FREE OpenSky Network API.
No registration required, completely legal and open source.

Free tier limitations:
- 1000 requests per day (anonymous)
- 4000 requests per day (with free account)
- Rate limit: ~10 requests per minute

Author: AI Assistant
License: MIT
"""

import requests
import json
import csv
import time
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class FlightData:
    """Simple flight data structure"""
    icao24: str
    callsign: Optional[str]
    origin_country: str
    longitude: Optional[float]
    latitude: Optional[float]
    altitude: Optional[float]
    on_ground: bool
    velocity: Optional[float]
    heading: Optional[float]
    last_contact: Optional[int]

class FreeFlightScraper:
    """
    Free flight data scraper using OpenSky Network API
    No API key required - completely free to use
    """
    
    def __init__(self, use_account: bool = False, username: str = None, password: str = None):
        self.base_url = "https://opensky-network.org/api"
        self.session = requests.Session()
        self.request_count = 0
        self.last_request_time = 0
        
        # Optional: Use free account for higher limits
        if use_account and username and password:
            self.session.auth = (username, password)
            self.daily_limit = 4000
            print(f"✅ Using OpenSky account: {username}")
            print("📈 Daily limit: 4000 requests")
        else:
            self.daily_limit = 1000
            print("ℹ️  Using OpenSky Network anonymously")
            print("📊 Daily limit: 1000 requests (no registration needed)")
        
        print("🌐 Data source: OpenSky Network (Free & Legal)")
        print("⚡ Rate limit: ~10 requests per minute")
    
    def _rate_limit(self):
        """Implement rate limiting to respect API limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # Wait at least 6 seconds between requests (10 requests/minute)
        if time_since_last < 6:
            wait_time = 6 - time_since_last
            print(f"⏳ Rate limiting... waiting {wait_time:.1f}s")
            time.sleep(wait_time)
        
        self.last_request_time = time.time()
        self.request_count += 1
        
        print(f"📡 Request #{self.request_count}/{self.daily_limit}")
    
    def get_all_flights(self) -> List[FlightData]:
        """
        Get all current flights worldwide
        Uses 1 API request
        """
        print("\n🌍 Fetching worldwide flight data...")
        self._rate_limit()
        
        try:
            response = self.session.get(f"{self.base_url}/states/all", timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data or 'states' not in data or not data['states']:
                print("❌ No flight data available")
                return []
            
            flights = []
            for state in data['states']:
                flight = FlightData(
                    icao24=state[0],
                    callsign=state[1].strip() if state[1] else None,
                    origin_country=state[2],
                    longitude=state[5],
                    latitude=state[6],
                    altitude=state[7],
                    on_ground=state[8],
                    velocity=state[9],
                    heading=state[10],
                    last_contact=state[4]
                )
                flights.append(flight)
            
            print(f"✅ Retrieved {len(flights)} flights")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_flights_in_area(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> List[FlightData]:
        """
        Get flights in a specific geographic area
        Uses 1 API request
        
        Example coordinates:
        - New York: (40.0, -75.0, 41.5, -73.0)
        - London: (51.0, -1.0, 52.0, 1.0)
        - Tokyo: (35.0, 139.0, 36.0, 140.5)
        """
        print(f"\n📍 Fetching flights in area: ({min_lat}, {min_lon}) to ({max_lat}, {max_lon})")
        self._rate_limit()
        
        params = {
            'lamin': min_lat,
            'lomin': min_lon,
            'lamax': max_lat,
            'lomax': max_lon
        }
        
        try:
            response = self.session.get(f"{self.base_url}/states/all", params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data or 'states' not in data:
                print("❌ No flights found in this area")
                return []
            
            flights = []
            for state in data['states']:
                flight = FlightData(
                    icao24=state[0],
                    callsign=state[1].strip() if state[1] else None,
                    origin_country=state[2],
                    longitude=state[5],
                    latitude=state[6],
                    altitude=state[7],
                    on_ground=state[8],
                    velocity=state[9],
                    heading=state[10],
                    last_contact=state[4]
                )
                flights.append(flight)
            
            print(f"✅ Found {len(flights)} flights in area")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_popular_regions(self) -> Dict[str, List[FlightData]]:
        """
        Get flights from popular regions (uses 3 API requests)
        """
        regions = {
            'USA East Coast': (35.0, -85.0, 45.0, -65.0),
            'Western Europe': (45.0, -10.0, 60.0, 15.0),
            'East Asia': (30.0, 120.0, 45.0, 145.0)
        }
        
        regional_flights = {}
        
        for region_name, (min_lat, min_lon, max_lat, max_lon) in regions.items():
            print(f"\n🗺️  Getting flights for {region_name}...")
            flights = self.get_flights_in_area(min_lat, min_lon, max_lat, max_lon)
            regional_flights[region_name] = flights
            
            if flights:
                print(f"   📊 {len(flights)} flights active")
        
        return regional_flights
    
    def export_to_json(self, flights: List[FlightData], filename: str = None) -> str:
        """Export flights to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flights_free_{timestamp}.json"
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'OpenSky Network (Free API)',
            'count': len(flights),
            'flights': []
        }
        
        for flight in flights:
            flight_dict = {
                'icao24': flight.icao24,
                'callsign': flight.callsign,
                'country': flight.origin_country,
                'position': {
                    'latitude': flight.latitude,
                    'longitude': flight.longitude,
                    'altitude_m': flight.altitude
                },
                'on_ground': flight.on_ground,
                'velocity_ms': flight.velocity,
                'heading_deg': flight.heading,
                'last_contact': flight.last_contact
            }
            data['flights'].append(flight_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"💾 Exported {len(flights)} flights to {filename}")
        return filename
    
    def export_to_csv(self, flights: List[FlightData], filename: str = None) -> str:
        """Export flights to CSV file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flights_free_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'icao24', 'callsign', 'country', 'latitude', 'longitude',
                'altitude_m', 'on_ground', 'velocity_ms', 'heading_deg', 'last_contact'
            ])
            
            # Data
            for flight in flights:
                writer.writerow([
                    flight.icao24, flight.callsign, flight.origin_country,
                    flight.latitude, flight.longitude, flight.altitude,
                    flight.on_ground, flight.velocity, flight.heading, flight.last_contact
                ])
        
        print(f"📝 Exported {len(flights)} flights to {filename}")
        return filename
    
    def show_statistics(self, flights: List[FlightData]) -> None:
        """Display flight statistics"""
        if not flights:
            print("❌ No flights to analyze")
            return
        
        total = len(flights)
        airborne = sum(1 for f in flights if not f.on_ground)
        grounded = total - airborne
        
        print(f"\n📊 FLIGHT STATISTICS")
        print(f"═══════════════════")
        print(f"Total aircraft: {total:,}")
        print(f"✈️  Airborne: {airborne:,}")
        print(f"🛬 On ground: {grounded:,}")
        
        # Country breakdown
        countries = {}
        for flight in flights:
            country = flight.origin_country
            countries[country] = countries.get(country, 0) + 1
        
        print(f"\n🌍 TOP COUNTRIES:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:10]:
            percentage = (count / total) * 100
            print(f"   {country}: {count} ({percentage:.1f}%)")
        
        # Altitude analysis for airborne flights
        airborne_flights = [f for f in flights if not f.on_ground and f.altitude]
        if airborne_flights:
            altitudes = [f.altitude for f in airborne_flights]
            avg_alt = sum(altitudes) / len(altitudes)
            max_alt = max(altitudes)
            
            print(f"\n🔺 ALTITUDE ANALYSIS:")
            print(f"   Average: {avg_alt:.0f}m ({avg_alt * 3.28:.0f}ft)")
            print(f"   Maximum: {max_alt:.0f}m ({max_alt * 3.28:.0f}ft)")
        
        print(f"\n📡 API Usage: {self.request_count}/{self.daily_limit} requests today")

def main():
    """Main demo function"""
    print("🛩️  FREE FLIGHT DATA SCRAPER")
    print("═" * 50)
    print("Using OpenSky Network - No API key needed!")
    print()
    
    # Initialize scraper
    scraper = FreeFlightScraper()
    
    # Example 1: Get worldwide data
    print("\n" + "="*50)
    print("📡 EXAMPLE 1: Worldwide Flight Data")
    print("="*50)
    
    all_flights = scraper.get_all_flights()
    
    if all_flights:
        # Show some sample flights
        print(f"\n✈️  SAMPLE FLIGHTS:")
        for i, flight in enumerate(all_flights[:5]):
            status = "🛬 On ground" if flight.on_ground else "✈️  Airborne"
            print(f"{i+1}. {flight.callsign or 'Unknown'} ({flight.icao24})")
            print(f"   Country: {flight.origin_country}")
            print(f"   Status: {status}")
            if flight.latitude and flight.longitude:
                print(f"   Position: {flight.latitude:.4f}, {flight.longitude:.4f}")
            if flight.altitude and not flight.on_ground:
                print(f"   Altitude: {flight.altitude:.0f}m ({flight.altitude * 3.28:.0f}ft)")
            print()
        
        # Show statistics
        scraper.show_statistics(all_flights)
        
        # Export data
        print(f"\n💾 EXPORTING DATA:")
        json_file = scraper.export_to_json(all_flights)
        csv_file = scraper.export_to_csv(all_flights)
    
    # Example 2: Regional data (if we have requests left)
    if scraper.request_count < scraper.daily_limit - 3:
        print("\n" + "="*50)
        print("📡 EXAMPLE 2: Regional Flight Data")
        print("="*50)
        
        regional_data = scraper.get_popular_regions()
        
        for region, flights in regional_data.items():
            if flights:
                print(f"\n🗺️  {region}: {len(flights)} flights")
                scraper.export_to_json(flights, f"{region.lower().replace(' ', '_')}_flights.json")
    else:
        print(f"\n⚠️  Skipping regional data to conserve API requests")
        print(f"   Current usage: {scraper.request_count}/{scraper.daily_limit}")
    
    print(f"\n" + "="*50)
    print("✅ SCRAPING COMPLETE!")
    print("="*50)
    print("📁 Generated files:")
    print("   - flights_free_[timestamp].json")
    print("   - flights_free_[timestamp].csv")
    print(f"📊 API requests used: {scraper.request_count}/{scraper.daily_limit}")
    print("🔄 Reset: Daily at midnight UTC")

if __name__ == "__main__":
    main()