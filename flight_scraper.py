#!/usr/bin/env python3
"""
Flight Data Scraper
==================

A comprehensive flight data scraper supporting multiple data sources:
1. OpenSky Network API (Free, legal, open source)
2. Flightradar24 API (Requires subscription)
3. Educational web scraping examples (with disclaimers)

Author: AI Assistant
License: MIT
"""

import requests
import asyncio
import aiohttp
import json
import csv
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class FlightData:
    """Data class for flight information"""
    icao24: str
    callsign: Optional[str]
    origin_country: str
    time_position: Optional[int]
    last_contact: Optional[int]
    longitude: Optional[float]
    latitude: Optional[float]
    baro_altitude: Optional[float]
    on_ground: bool
    velocity: Optional[float]
    true_track: Optional[float]
    vertical_rate: Optional[float]
    sensors: Optional[List[int]]
    geo_altitude: Optional[float]
    squawk: Optional[str]
    spi: bool
    position_source: int

class OpenSkyNetworkScraper:
    """
    Legal flight data scraper using OpenSky Network API
    Free for research and non-commercial use
    """
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        self.base_url = "https://opensky-network.org/api"
        self.username = username or os.getenv('OPENSKY_USERNAME')
        self.password = password or os.getenv('OPENSKY_PASSWORD')
        self.session = requests.Session()
        
        if self.username and self.password:
            self.session.auth = (self.username, self.password)
            print("✓ Authenticated with OpenSky Network")
        else:
            print("ℹ Using OpenSky Network without authentication (limited requests)")
    
    def get_states(self, icao24: Optional[str] = None, time: Optional[int] = None) -> List[FlightData]:
        """
        Get current aircraft states
        
        Args:
            icao24: ICAO24 address of aircraft (optional)
            time: Unix timestamp for historical data (optional)
            
        Returns:
            List of FlightData objects
        """
        url = f"{self.base_url}/states/all"
        params = {}
        
        if icao24:
            params['icao24'] = icao24
        if time:
            params['time'] = time
            
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data or 'states' not in data or not data['states']:
                print("No flight data found")
                return []
            
            flights = []
            for state in data['states']:
                flight = FlightData(
                    icao24=state[0],
                    callsign=state[1].strip() if state[1] else None,
                    origin_country=state[2],
                    time_position=state[3],
                    last_contact=state[4],
                    longitude=state[5],
                    latitude=state[6],
                    baro_altitude=state[7],
                    on_ground=state[8],
                    velocity=state[9],
                    true_track=state[10],
                    vertical_rate=state[11],
                    sensors=state[12],
                    geo_altitude=state[13],
                    squawk=state[14],
                    spi=state[15],
                    position_source=state[16]
                )
                flights.append(flight)
            
            print(f"✓ Retrieved {len(flights)} flight records")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data from OpenSky: {e}")
            return []
    
    def get_flights_by_bbox(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> List[FlightData]:
        """
        Get flights within a bounding box
        
        Args:
            min_lat: Minimum latitude
            min_lon: Minimum longitude  
            max_lat: Maximum latitude
            max_lon: Maximum longitude
            
        Returns:
            List of FlightData objects
        """
        url = f"{self.base_url}/states/all"
        params = {
            'lamin': min_lat,
            'lomin': min_lon,
            'lamax': max_lat,
            'lomax': max_lon
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if not data or 'states' not in data:
                return []
            
            flights = []
            for state in data['states']:
                flight = FlightData(
                    icao24=state[0],
                    callsign=state[1].strip() if state[1] else None,
                    origin_country=state[2],
                    time_position=state[3],
                    last_contact=state[4],
                    longitude=state[5],
                    latitude=state[6],
                    baro_altitude=state[7],
                    on_ground=state[8],
                    velocity=state[9],
                    true_track=state[10],
                    vertical_rate=state[11],
                    sensors=state[12],
                    geo_altitude=state[13],
                    squawk=state[14],
                    spi=state[15],
                    position_source=state[16]
                )
                flights.append(flight)
            
            print(f"✓ Found {len(flights)} flights in bounding box")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching bbox data: {e}")
            return []

class Flightradar24APIScraper:
    """
    Official Flightradar24 API integration
    Requires subscription and API key
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('FR24_API_KEY')
        self.base_url = "https://api.flightradar24.com/v1"
        
        if not self.api_key:
            print("⚠ Flightradar24 API key not provided. Set FR24_API_KEY environment variable.")
        else:
            print("✓ Flightradar24 API configured")
    
    def get_flights(self, bounds: Optional[Dict] = None) -> List[Dict]:
        """
        Get flight data using official FR24 API
        
        Args:
            bounds: Geographic bounds dictionary with 'north', 'south', 'east', 'west'
            
        Returns:
            List of flight dictionaries
        """
        if not self.api_key:
            print("✗ API key required for Flightradar24 access")
            return []
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json'
        }
        
        params = {}
        if bounds:
            params.update(bounds)
        
        try:
            response = requests.get(f"{self.base_url}/flights", headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            print(f"✓ Retrieved {len(data.get('flights', []))} flights from FR24 API")
            return data.get('flights', [])
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error accessing FR24 API: {e}")
            return []

class EducationalWebScraper:
    """
    Educational web scraping examples with proper disclaimers
    ⚠ FOR EDUCATIONAL PURPOSES ONLY ⚠
    Direct web scraping may violate Terms of Service
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        print("⚠ Educational scraper initialized - Use responsibly and respect ToS")
    
    def scrape_example_only(self) -> Dict:
        """
        Example scraping function - FOR EDUCATIONAL PURPOSES ONLY
        
        ⚠ WARNING: This is for educational demonstration only.
        Direct scraping of Flightradar24 violates their Terms of Service.
        Use the official API instead.
        """
        print("⚠ EDUCATIONAL EXAMPLE - DO NOT USE IN PRODUCTION")
        print("This demonstrates web scraping concepts only.")
        print("Always use official APIs for real applications.")
        
        # This is just a demonstration of the concept
        example_data = {
            "disclaimer": "This is an educational example only",
            "recommendation": "Use OpenSky Network API or FR24 official API",
            "legal_note": "Direct scraping may violate Terms of Service",
            "example_structure": {
                "flights": [],
                "timestamp": datetime.now().isoformat(),
                "source": "Educational demonstration"
            }
        }
        
        return example_data

class FlightDataExporter:
    """Export flight data to various formats"""
    
    @staticmethod
    def to_json(flights: List[FlightData], filename: str) -> None:
        """Export flights to JSON format"""
        data = []
        for flight in flights:
            flight_dict = {
                'icao24': flight.icao24,
                'callsign': flight.callsign,
                'origin_country': flight.origin_country,
                'time_position': flight.time_position,
                'last_contact': flight.last_contact,
                'longitude': flight.longitude,
                'latitude': flight.latitude,
                'baro_altitude': flight.baro_altitude,
                'on_ground': flight.on_ground,
                'velocity': flight.velocity,
                'true_track': flight.true_track,
                'vertical_rate': flight.vertical_rate,
                'geo_altitude': flight.geo_altitude,
                'squawk': flight.squawk,
                'spi': flight.spi,
                'position_source': flight.position_source
            }
            data.append(flight_dict)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'count': len(flights),
                'flights': data
            }, f, indent=2, default=str)
        
        print(f"✓ Exported {len(flights)} flights to {filename}")
    
    @staticmethod
    def to_csv(flights: List[FlightData], filename: str) -> None:
        """Export flights to CSV format"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            header = [
                'icao24', 'callsign', 'origin_country', 'time_position',
                'last_contact', 'longitude', 'latitude', 'baro_altitude',
                'on_ground', 'velocity', 'true_track', 'vertical_rate',
                'geo_altitude', 'squawk', 'spi', 'position_source'
            ]
            writer.writerow(header)
            
            # Write data
            for flight in flights:
                row = [
                    flight.icao24, flight.callsign, flight.origin_country,
                    flight.time_position, flight.last_contact, flight.longitude,
                    flight.latitude, flight.baro_altitude, flight.on_ground,
                    flight.velocity, flight.true_track, flight.vertical_rate,
                    flight.geo_altitude, flight.squawk, flight.spi,
                    flight.position_source
                ]
                writer.writerow(row)
        
        print(f"✓ Exported {len(flights)} flights to {filename}")

class FlightScraper:
    """Main flight scraper class combining all data sources"""
    
    def __init__(self):
        self.opensky = OpenSkyNetworkScraper()
        self.fr24_api = Flightradar24APIScraper()
        self.educational = EducationalWebScraper()
        self.exporter = FlightDataExporter()
    
    def get_all_flights(self, use_opensky: bool = True, use_fr24_api: bool = False) -> List[FlightData]:
        """
        Get flights from all available sources
        
        Args:
            use_opensky: Whether to use OpenSky Network (recommended)
            use_fr24_api: Whether to use FR24 API (requires subscription)
            
        Returns:
            Combined list of flight data
        """
        all_flights = []
        
        if use_opensky:
            print("\n📡 Fetching from OpenSky Network...")
            opensky_flights = self.opensky.get_states()
            all_flights.extend(opensky_flights)
        
        if use_fr24_api:
            print("\n📡 Fetching from Flightradar24 API...")
            fr24_flights = self.fr24_api.get_flights()
            # Note: FR24 API returns different format, would need conversion
            print(f"ℹ FR24 API returned {len(fr24_flights)} flights (format conversion needed)")
        
        return all_flights
    
    def get_flights_by_region(self, region: str) -> List[FlightData]:
        """
        Get flights by predefined regions
        
        Args:
            region: Region name ('europe', 'usa', 'asia', 'custom')
            
        Returns:
            List of flight data for the region
        """
        regions = {
            'europe': {
                'min_lat': 35.0, 'max_lat': 70.0,
                'min_lon': -25.0, 'max_lon': 40.0
            },
            'usa': {
                'min_lat': 25.0, 'max_lat': 49.0,
                'min_lon': -125.0, 'max_lon': -66.0
            },
            'asia': {
                'min_lat': -10.0, 'max_lat': 55.0,
                'min_lon': 60.0, 'max_lon': 180.0
            }
        }
        
        if region not in regions:
            print(f"✗ Unknown region '{region}'. Available: {list(regions.keys())}")
            return []
        
        bbox = regions[region]
        print(f"\n📍 Fetching flights for {region.title()} region...")
        
        return self.opensky.get_flights_by_bbox(
            bbox['min_lat'], bbox['min_lon'],
            bbox['max_lat'], bbox['max_lon']
        )
    
    def export_data(self, flights: List[FlightData], format_type: str = 'json', filename: Optional[str] = None) -> None:
        """
        Export flight data to file
        
        Args:
            flights: List of flight data
            format_type: Export format ('json' or 'csv')
            filename: Output filename (auto-generated if None)
        """
        if not flights:
            print("✗ No flight data to export")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"flights_{timestamp}.{format_type}"
        
        if format_type.lower() == 'json':
            self.exporter.to_json(flights, filename)
        elif format_type.lower() == 'csv':
            self.exporter.to_csv(flights, filename)
        else:
            print(f"✗ Unsupported format: {format_type}")

def main():
    """Main function demonstrating flight scraper usage"""
    print("=" * 60)
    print("🛩️  FLIGHT DATA SCRAPER")
    print("=" * 60)
    print()
    
    # Initialize scraper
    scraper = FlightScraper()
    
    # Example 1: Get all flights (OpenSky Network)
    print("📋 Example 1: Getting global flight data...")
    flights = scraper.get_all_flights(use_opensky=True, use_fr24_api=False)
    
    if flights:
        print(f"\n✓ Retrieved {len(flights)} flights")
        
        # Show sample data
        print("\n📊 Sample flight data:")
        for i, flight in enumerate(flights[:3]):  # Show first 3 flights
            print(f"{i+1}. {flight.callsign or 'N/A'} ({flight.icao24}) - {flight.origin_country}")
            if flight.latitude and flight.longitude:
                print(f"   Position: {flight.latitude:.4f}, {flight.longitude:.4f}")
            if flight.baro_altitude:
                print(f"   Altitude: {flight.baro_altitude:.0f} m")
        
        # Export data
        print(f"\n💾 Exporting data...")
        scraper.export_data(flights, 'json')
        scraper.export_data(flights, 'csv')
    
    # Example 2: Regional data
    print(f"\n📋 Example 2: Getting regional flight data...")
    europe_flights = scraper.get_flights_by_region('europe')
    
    if europe_flights:
        print(f"✓ Found {len(europe_flights)} flights over Europe")
        scraper.export_data(europe_flights, 'json', 'europe_flights.json')
    
    # Educational disclaimer
    print(f"\n" + "=" * 60)
    print("ℹ️  LEGAL NOTICE")
    print("=" * 60)
    print("This scraper uses legal APIs and open data sources:")
    print("✓ OpenSky Network: Free, open source flight data")
    print("✓ Flightradar24 API: Official paid API")
    print("⚠ Direct web scraping may violate Terms of Service")
    print("Always prefer official APIs for production use")
    print("=" * 60)

if __name__ == "__main__":
    main()