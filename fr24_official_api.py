#!/usr/bin/env python3
"""
Official Flightradar24 API Integration
=====================================

This script uses the OFFICIAL Flightradar24 API service.
Requires subscription but is completely legal and reliable.

Sign up at: https://www.flightradar24.com/commercial-services/api
"""

import requests
import json
import csv
import time
from datetime import datetime
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class FlightRadar24API:
    """
    Official Flightradar24 API client
    Requires valid API subscription and key
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('FR24_API_KEY')
        
        # FR24 API endpoints (these are examples - check actual documentation)
        self.base_url = "https://api.flightradar24.com/v1"
        
        if not self.api_key:
            print("❌ Flightradar24 API key required!")
            print("📝 Get your API key at: https://www.flightradar24.com/commercial-services/api")
            print("💡 Set environment variable: FR24_API_KEY=your_api_key")
            return
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'User-Agent': 'FR24-Python-Client/1.0'
        }
        
        print("✅ Flightradar24 API initialized")
        print("🌐 Using official API - fully legal and compliant")
    
    def test_connection(self) -> bool:
        """Test API connection and authentication"""
        if not self.api_key:
            return False
        
        try:
            # Test endpoint (replace with actual FR24 test endpoint)
            response = requests.get(
                f"{self.base_url}/test", 
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ API connection successful")
                return True
            else:
                print(f"❌ API test failed: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_flights_in_bounds(self, north: float, south: float, east: float, west: float) -> List[Dict]:
        """
        Get flights within geographic bounds
        
        Args:
            north: Northern boundary latitude
            south: Southern boundary latitude  
            east: Eastern boundary longitude
            west: Western boundary longitude
        """
        if not self.api_key:
            return []
        
        params = {
            'bounds': f"{north},{south},{east},{west}",
            'format': 'json'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}/flights",
                headers=self.headers,
                params=params,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            flights = data.get('flights', [])
            print(f"✅ Retrieved {len(flights)} flights from FR24 API")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"❌ API error: {e}")
            return []
    
    def get_flight_details(self, flight_id: str) -> Dict:
        """Get detailed information for a specific flight"""
        if not self.api_key:
            return {}
        
        try:
            response = requests.get(
                f"{self.base_url}/flights/{flight_id}",
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            flight_data = response.json()
            
            print(f"✅ Retrieved details for flight {flight_id}")
            return flight_data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting flight details: {e}")
            return {}
    
    def get_airport_flights(self, airport_code: str) -> List[Dict]:
        """Get flights for a specific airport"""
        if not self.api_key:
            return []
        
        try:
            response = requests.get(
                f"{self.base_url}/airports/{airport_code}/flights",
                headers=self.headers,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            flights = data.get('flights', [])
            print(f"✅ Retrieved {len(flights)} flights for {airport_code}")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting airport flights: {e}")
            return []
    
    def export_to_json(self, data: List[Dict], filename: str = None) -> str:
        """Export data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"fr24_data_{timestamp}.json"
        
        export_data = {
            'timestamp': datetime.now().isoformat(),
            'source': 'Flightradar24 Official API',
            'count': len(data),
            'data': data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        print(f"💾 Exported {len(data)} records to {filename}")
        return filename

def demo_official_api():
    """Demonstrate official FR24 API usage"""
    print("🛩️  FLIGHTRADAR24 OFFICIAL API")
    print("=" * 50)
    
    # Initialize API client
    fr24 = FlightRadar24API()
    
    if not fr24.api_key:
        print("\n💡 TO USE THIS SCRIPT:")
        print("1. Subscribe to FR24 API: https://www.flightradar24.com/commercial-services/api")
        print("2. Get your API key from the dashboard")
        print("3. Set environment variable: FR24_API_KEY=your_key")
        print("4. Run this script again")
        return
    
    # Test connection
    if not fr24.test_connection():
        return
    
    # Example: Get flights around New York
    print("\n📍 Getting flights around New York...")
    ny_flights = fr24.get_flights_in_bounds(
        north=41.0, south=40.0,
        east=-73.0, west=-75.0
    )
    
    if ny_flights:
        print(f"\n✈️  Sample flights around NYC:")
        for i, flight in enumerate(ny_flights[:5]):
            print(f"{i+1}. {flight.get('callsign', 'N/A')} - {flight.get('airline', 'N/A')}")
        
        # Export data
        fr24.export_to_json(ny_flights, "nyc_flights_fr24.json")
    
    # Example: Get flights from JFK airport
    print("\n🛫 Getting flights from JFK airport...")
    jfk_flights = fr24.get_airport_flights("JFK")
    
    if jfk_flights:
        print(f"✅ Found {len(jfk_flights)} flights at JFK")
        fr24.export_to_json(jfk_flights, "jfk_flights_fr24.json")

if __name__ == "__main__":
    demo_official_api()