#!/usr/bin/env python3
"""
Flightradar24 Official API Client
================================

A comprehensive Python client for the Flightradar24 Official API.
Requires valid API subscription and token.

Features:
- Live flight data
- Flight tracking
- Airport information
- Airline data
- Historical flight data
- Aircraft information
- Data export (JSON, CSV)
- Rate limiting
- Error handling

Author: AI Assistant
License: MIT
"""

import requests
import json
import csv
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class FlightInfo:
    """Flight information data structure"""
    flight_id: str
    callsign: str
    origin: Dict
    destination: Dict
    aircraft: Dict
    status: str
    departure_time: Optional[str]
    arrival_time: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    altitude: Optional[int]
    speed: Optional[int]
    heading: Optional[int]

class FlightRadar24Client:
    """
    Official Flightradar24 API Client
    
    Provides access to all FR24 API endpoints with proper authentication,
    rate limiting, and error handling.
    """
    
    def __init__(self, api_token: str = None):
        """
        Initialize the FR24 API client
        
        Args:
            api_token: Your FR24 API token (can also use FR24_API_TOKEN env variable)
        """
        self.api_token = api_token or os.getenv('FR24_API_TOKEN')
        self.base_url = "https://fr24api.flightradar24.com/v1"
        
        if not self.api_token:
            raise ValueError("FR24 API token is required. Set FR24_API_TOKEN environment variable or pass token directly.")
        
        # Setup session with authentication
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_token}',
            'Accept': 'application/json',
            'User-Agent': 'FR24-Python-Client/1.0',
            'Content-Type': 'application/json'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms between requests
        
        logger.info("✅ Flightradar24 API client initialized")
        logger.info("🌐 Using official FR24 API - fully legal and compliant")
    
    def _rate_limit(self):
        """Implement rate limiting between API calls"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make authenticated request to FR24 API
        
        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            
        Returns:
            JSON response as dictionary
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                logger.error("❌ Authentication failed. Check your API token.")
                raise ValueError("Invalid API token")
            elif response.status_code == 429:
                logger.error("❌ Rate limit exceeded. Wait before making more requests.")
                raise Exception("Rate limit exceeded")
            else:
                logger.error(f"❌ HTTP error {response.status_code}: {response.text}")
                raise
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Request failed: {e}")
            raise
    
    def test_connection(self) -> bool:
        """
        Test API connection and authentication
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get a simple endpoint to test authentication
            self._make_request('airlines')
            logger.info("✅ API connection test successful")
            return True
        except Exception as e:
            logger.error(f"❌ API connection test failed: {e}")
            return False
    
    def get_live_flights(self, bounds: Dict = None, aircraft_type: str = None) -> List[Dict]:
        """
        Get live flight data
        
        Args:
            bounds: Geographic bounds {'north': lat, 'south': lat, 'east': lon, 'west': lon}
            aircraft_type: Filter by aircraft type (e.g., 'B738', 'A320')
            
        Returns:
            List of flight dictionaries
        """
        endpoint = "flights"
        params = {}
        
        if bounds:
            params.update(bounds)
        if aircraft_type:
            params['aircraft_type'] = aircraft_type
        
        logger.info(f"🛩️  Fetching live flights...")
        data = self._make_request(endpoint, params)
        
        flights = data.get('data', [])
        logger.info(f"✅ Retrieved {len(flights)} live flights")
        return flights
    
    def get_flight_details(self, flight_id: str) -> Dict:
        """
        Get detailed information for a specific flight
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight details dictionary
        """
        endpoint = f"flights/{flight_id}"
        
        logger.info(f"🔍 Getting details for flight {flight_id}")
        data = self._make_request(endpoint)
        
        logger.info(f"✅ Retrieved details for flight {flight_id}")
        return data
    
    def get_flight_track(self, flight_id: str) -> Dict:
        """
        Get flight track (historical positions)
        
        Args:
            flight_id: Flight identifier
            
        Returns:
            Flight track data
        """
        endpoint = f"flights/{flight_id}/track"
        
        logger.info(f"📍 Getting track for flight {flight_id}")
        data = self._make_request(endpoint)
        
        track_points = data.get('data', [])
        logger.info(f"✅ Retrieved {len(track_points)} track points")
        return data
    
    def get_airport_info(self, airport_code: str) -> Dict:
        """
        Get airport information
        
        Args:
            airport_code: IATA or ICAO airport code (e.g., 'JFK', 'KJFK')
            
        Returns:
            Airport information dictionary
        """
        endpoint = f"airports/{airport_code}"
        
        logger.info(f"🏢 Getting info for airport {airport_code}")
        data = self._make_request(endpoint)
        
        logger.info(f"✅ Retrieved info for {airport_code}")
        return data
    
    def get_airport_arrivals(self, airport_code: str, limit: int = 100) -> List[Dict]:
        """
        Get arriving flights for an airport
        
        Args:
            airport_code: IATA or ICAO airport code
            limit: Maximum number of flights to return
            
        Returns:
            List of arriving flights
        """
        endpoint = f"airports/{airport_code}/arrivals"
        params = {'limit': limit}
        
        logger.info(f"🛬 Getting arrivals for {airport_code}")
        data = self._make_request(endpoint, params)
        
        arrivals = data.get('data', [])
        logger.info(f"✅ Retrieved {len(arrivals)} arrivals")
        return arrivals
    
    def get_airport_departures(self, airport_code: str, limit: int = 100) -> List[Dict]:
        """
        Get departing flights for an airport
        
        Args:
            airport_code: IATA or ICAO airport code
            limit: Maximum number of flights to return
            
        Returns:
            List of departing flights
        """
        endpoint = f"airports/{airport_code}/departures"
        params = {'limit': limit}
        
        logger.info(f"🛫 Getting departures for {airport_code}")
        data = self._make_request(endpoint, params)
        
        departures = data.get('data', [])
        logger.info(f"✅ Retrieved {len(departures)} departures")
        return departures
    
    def get_airline_info(self, airline_code: str) -> Dict:
        """
        Get airline information
        
        Args:
            airline_code: IATA or ICAO airline code (e.g., 'AA', 'AAL')
            
        Returns:
            Airline information dictionary
        """
        endpoint = f"airlines/{airline_code}"
        
        logger.info(f"✈️  Getting info for airline {airline_code}")
        data = self._make_request(endpoint)
        
        logger.info(f"✅ Retrieved info for airline {airline_code}")
        return data
    
    def get_airline_fleet(self, airline_code: str) -> List[Dict]:
        """
        Get airline fleet information
        
        Args:
            airline_code: IATA or ICAO airline code
            
        Returns:
            List of aircraft in the fleet
        """
        endpoint = f"airlines/{airline_code}/fleet"
        
        logger.info(f"🚁 Getting fleet for airline {airline_code}")
        data = self._make_request(endpoint)
        
        fleet = data.get('data', [])
        logger.info(f"✅ Retrieved {len(fleet)} aircraft in fleet")
        return fleet
    
    def search_flights(self, query: str, limit: int = 50) -> List[Dict]:
        """
        Search for flights by callsign, route, or other criteria
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of matching flights
        """
        endpoint = "search"
        params = {'q': query, 'limit': limit}
        
        logger.info(f"🔍 Searching flights for: {query}")
        data = self._make_request(endpoint, params)
        
        results = data.get('data', [])
        logger.info(f"✅ Found {len(results)} matching flights")
        return results
    
    def get_aircraft_info(self, registration: str) -> Dict:
        """
        Get aircraft information by registration
        
        Args:
            registration: Aircraft registration (e.g., 'N12345')
            
        Returns:
            Aircraft information dictionary
        """
        endpoint = f"aircraft/{registration}"
        
        logger.info(f"✈️  Getting info for aircraft {registration}")
        data = self._make_request(endpoint)
        
        logger.info(f"✅ Retrieved info for aircraft {registration}")
        return data
    
    def get_playback_data(self, flight_id: str, timestamp: int) -> Dict:
        """
        Get historical playback data for a flight
        
        Args:
            flight_id: Flight identifier
            timestamp: Unix timestamp for playback
            
        Returns:
            Playback data
        """
        endpoint = f"playback/{flight_id}"
        params = {'timestamp': timestamp}
        
        logger.info(f"📼 Getting playback data for flight {flight_id}")
        data = self._make_request(endpoint, params)
        
        logger.info(f"✅ Retrieved playback data")
        return data
    
    def export_to_json(self, data: Any, filename: str = None) -> str:
        """
        Export data to JSON file
        
        Args:
            data: Data to export
            filename: Output filename (auto-generated if None)
            
        Returns:
            Generated filename
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fr24_data_{timestamp}.json"
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Flightradar24 Official API',
            'data_type': type(data).__name__,
            'count': len(data) if isinstance(data, (list, dict)) else 1,
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"💾 Exported data to {filename}")
        return filename
    
    def export_flights_to_csv(self, flights: List[Dict], filename: str = None) -> str:
        """
        Export flight data to CSV file
        
        Args:
            flights: List of flight data
            filename: Output filename (auto-generated if None)
            
        Returns:
            Generated filename
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fr24_flights_{timestamp}.csv"
        
        if not flights:
            logger.warning("⚠️  No flights to export")
            return filename
        
        # Extract common fields
        fieldnames = set()
        for flight in flights:
            fieldnames.update(flight.keys())
        
        fieldnames = sorted(list(fieldnames))
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for flight in flights:
                # Flatten nested dictionaries
                flattened = {}
                for key, value in flight.items():
                    if isinstance(value, dict):
                        for subkey, subvalue in value.items():
                            flattened[f"{key}_{subkey}"] = subvalue
                    else:
                        flattened[key] = value
                
                writer.writerow({k: v for k, v in flattened.items() if k in fieldnames})
        
        logger.info(f"📝 Exported {len(flights)} flights to {filename}")
        return filename
    
    def get_statistics(self, flights: List[Dict]) -> Dict:
        """
        Generate statistics from flight data
        
        Args:
            flights: List of flight data
            
        Returns:
            Statistics dictionary
        """
        if not flights:
            return {'error': 'No flights provided'}
        
        stats = {
            'total_flights': len(flights),
            'timestamp': datetime.now().isoformat(),
            'airlines': {},
            'aircraft_types': {},
            'origins': {},
            'destinations': {},
            'status_counts': {}
        }
        
        for flight in flights:
            # Count airlines
            airline = flight.get('airline', {}).get('icao', 'Unknown')
            stats['airlines'][airline] = stats['airlines'].get(airline, 0) + 1
            
            # Count aircraft types
            aircraft_type = flight.get('aircraft', {}).get('model', 'Unknown')
            stats['aircraft_types'][aircraft_type] = stats['aircraft_types'].get(aircraft_type, 0) + 1
            
            # Count origins
            origin = flight.get('origin', {}).get('iata', 'Unknown')
            stats['origins'][origin] = stats['origins'].get(origin, 0) + 1
            
            # Count destinations
            destination = flight.get('destination', {}).get('iata', 'Unknown')
            stats['destinations'][destination] = stats['destinations'].get(destination, 0) + 1
            
            # Count status
            status = flight.get('status', 'Unknown')
            stats['status_counts'][status] = stats['status_counts'].get(status, 0) + 1
        
        # Sort by frequency
        for category in ['airlines', 'aircraft_types', 'origins', 'destinations', 'status_counts']:
            stats[category] = dict(sorted(stats[category].items(), key=lambda x: x[1], reverse=True)[:10])
        
        return stats

class FR24DataCollector:
    """
    High-level data collection class using FR24 API
    """
    
    def __init__(self, api_token: str = None):
        self.client = FlightRadar24Client(api_token)
    
    def collect_airport_data(self, airport_code: str) -> Dict:
        """
        Collect comprehensive data for an airport
        
        Args:
            airport_code: Airport IATA/ICAO code
            
        Returns:
            Complete airport data package
        """
        logger.info(f"🏢 Collecting comprehensive data for {airport_code}")
        
        data = {
            'airport_info': self.client.get_airport_info(airport_code),
            'arrivals': self.client.get_airport_arrivals(airport_code),
            'departures': self.client.get_airport_departures(airport_code),
            'timestamp': datetime.now().isoformat()
        }
        
        total_flights = len(data['arrivals']) + len(data['departures'])
        logger.info(f"✅ Collected data for {airport_code}: {total_flights} total flights")
        
        return data
    
    def collect_airline_data(self, airline_code: str) -> Dict:
        """
        Collect comprehensive data for an airline
        
        Args:
            airline_code: Airline IATA/ICAO code
            
        Returns:
            Complete airline data package
        """
        logger.info(f"✈️  Collecting comprehensive data for {airline_code}")
        
        data = {
            'airline_info': self.client.get_airline_info(airline_code),
            'fleet': self.client.get_airline_fleet(airline_code),
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Collected data for {airline_code}: {len(data['fleet'])} aircraft in fleet")
        
        return data
    
    def collect_region_flights(self, bounds: Dict, name: str = "Custom Region") -> Dict:
        """
        Collect flights in a geographic region
        
        Args:
            bounds: Geographic bounds dictionary
            name: Region name for identification
            
        Returns:
            Regional flight data package
        """
        logger.info(f"🗺️  Collecting flights for {name}")
        
        flights = self.client.get_live_flights(bounds=bounds)
        stats = self.client.get_statistics(flights)
        
        data = {
            'region_name': name,
            'bounds': bounds,
            'flights': flights,
            'statistics': stats,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"✅ Collected {len(flights)} flights for {name}")
        
        return data

def main():
    """
    Demonstration of FR24 API client usage
    """
    print("🛩️  FLIGHTRADAR24 OFFICIAL API CLIENT")
    print("=" * 60)
    
    try:
        # Initialize client
        client = FlightRadar24Client()
        
        # Test connection
        if not client.test_connection():
            print("❌ API connection failed. Check your token and try again.")
            return
        
        print("\n🎯 API CONNECTION SUCCESSFUL!")
        print("Now you can use all FR24 API features...")
        
        # Example 1: Get live flights in a region
        print("\n" + "="*50)
        print("📡 EXAMPLE 1: Live Flights in Region")
        print("="*50)
        
        # New York area bounds
        ny_bounds = {
            'north': 41.0,
            'south': 40.0,
            'east': -73.0,
            'west': -75.0
        }
        
        flights = client.get_live_flights(bounds=ny_bounds)
        if flights:
            print(f"\n✅ Found {len(flights)} flights around NYC")
            
            # Show sample flights
            print("\n🛩️  Sample flights:")
            for i, flight in enumerate(flights[:5]):
                callsign = flight.get('callsign', 'N/A')
                origin = flight.get('origin', {}).get('iata', 'N/A')
                destination = flight.get('destination', {}).get('iata', 'N/A')
                print(f"{i+1}. {callsign}: {origin} → {destination}")
            
            # Export data
            json_file = client.export_to_json(flights, "nyc_flights.json")
            csv_file = client.export_flights_to_csv(flights, "nyc_flights.csv")
            
            # Show statistics
            stats = client.get_statistics(flights)
            print(f"\n📊 Top airlines in NYC area:")
            for airline, count in list(stats['airlines'].items())[:5]:
                print(f"   {airline}: {count} flights")
        
        # Example 2: Airport data
        print("\n" + "="*50)
        print("🏢 EXAMPLE 2: Airport Data")
        print("="*50)
        
        airport_code = "JFK"
        collector = FR24DataCollector()
        airport_data = collector.collect_airport_data(airport_code)
        
        if airport_data:
            arrivals_count = len(airport_data['arrivals'])
            departures_count = len(airport_data['departures'])
            print(f"✅ {airport_code} Data:")
            print(f"   📥 Arrivals: {arrivals_count}")
            print(f"   📤 Departures: {departures_count}")
            
            # Export airport data
            client.export_to_json(airport_data, f"{airport_code.lower()}_data.json")
        
        print("\n" + "="*60)
        print("✅ DEMONSTRATION COMPLETE!")
        print("="*60)
        print("📁 Generated files:")
        print("   - nyc_flights.json")
        print("   - nyc_flights.csv")
        print("   - jfk_data.json")
        print("\n💡 Your FR24 API client is ready for production use!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 Setup instructions:")
        print("1. Get your FR24 API token from: https://www.flightradar24.com/commercial-services/api")
        print("2. Set environment variable: FR24_API_TOKEN=your_token")
        print("3. Run this script again")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    main()