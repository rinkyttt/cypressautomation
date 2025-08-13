#!/usr/bin/env python3
"""
Turkish Airlines A321neo Fleet Tracker
Fetches flight data for Turkish Airlines' A321neo aircraft using FlightRadar24 API
"""

import requests
import json
import csv
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from dataclasses import dataclass, asdict


@dataclass
class FlightData:
    """Data structure for flight information"""
    registration: str
    flight_number: str
    departure_airport: str
    arrival_airport: str
    departure_time: str
    arrival_time: str
    flight_duration: str
    aircraft_type: str
    status: str
    date: str


class FlightRadar24API:
    """FlightRadar24 API client for fetching aircraft and flight data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.flightradar24.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Turkish-Airlines-Fleet-Tracker/1.0"
        }
        
    def get_airline_fleet(self, airline_code: str = "TK") -> List[Dict]:
        """
        Retrieve fleet information for Turkish Airlines
        
        Args:
            airline_code: IATA code for Turkish Airlines (TK)
            
        Returns:
            List of aircraft in the fleet
        """
        url = f"{self.base_url}/common/v1/airline/fleet.json"
        params = {"airline": airline_code}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Filter for A321neo aircraft (type code: A21N)
            a321neo_fleet = [
                aircraft for aircraft in data.get("aircraft", [])
                if aircraft.get("type", "").upper() == "A21N"
            ]
            
            print(f"Found {len(a321neo_fleet)} A321neo aircraft in Turkish Airlines fleet")
            return a321neo_fleet
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fleet data: {e}")
            return []
    
    def get_aircraft_flights(self, registration: str, days_back: int = 30) -> List[FlightData]:
        """
        Retrieve flight history for a specific aircraft
        
        Args:
            registration: Aircraft registration number (e.g., TC-LTI)
            days_back: Number of days to look back for flight history
            
        Returns:
            List of FlightData objects
        """
        url = f"{self.base_url}/common/v1/flight/list.json"
        params = {
            "registration": registration,
            "from": int((datetime.now() - timedelta(days=days_back)).timestamp()),
            "to": int(datetime.now().timestamp())
        }
        
        flights = []
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            for flight in data.get("result", []):
                flight_data = FlightData(
                    registration=registration,
                    flight_number=flight.get("flight", ""),
                    departure_airport=flight.get("airport_origin", {}).get("iata", ""),
                    arrival_airport=flight.get("airport_destination", {}).get("iata", ""),
                    departure_time=self._format_timestamp(flight.get("time_scheduled_departure")),
                    arrival_time=self._format_timestamp(flight.get("time_scheduled_arrival")),
                    flight_duration=self._calculate_duration(
                        flight.get("time_scheduled_departure"),
                        flight.get("time_scheduled_arrival")
                    ),
                    aircraft_type="A21N",
                    status=flight.get("status", ""),
                    date=self._format_date(flight.get("time_scheduled_departure"))
                )
                flights.append(flight_data)
                
            print(f"Retrieved {len(flights)} flights for aircraft {registration}")
            return flights
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flights for {registration}: {e}")
            return []
    
    def _format_timestamp(self, timestamp: Optional[int]) -> str:
        """Convert Unix timestamp to readable format"""
        if not timestamp:
            return ""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    
    def _format_date(self, timestamp: Optional[int]) -> str:
        """Convert Unix timestamp to date format"""
        if not timestamp:
            return ""
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    
    def _calculate_duration(self, departure: Optional[int], arrival: Optional[int]) -> str:
        """Calculate flight duration from departure and arrival timestamps"""
        if not departure or not arrival:
            return ""
        
        duration_seconds = arrival - departure
        hours, remainder = divmod(duration_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"


class TurkishAirlinesFleetTracker:
    """Main class for tracking Turkish Airlines A321neo fleet"""
    
    def __init__(self, api_key: str):
        self.api = FlightRadar24API(api_key)
        self.all_flights = []
        
    def fetch_fleet_data(self, days_back: int = 30) -> List[FlightData]:
        """
        Fetch flight data for entire A321neo fleet
        
        Args:
            days_back: Number of days to look back for flight history
            
        Returns:
            List of all flight data
        """
        print("Fetching Turkish Airlines A321neo fleet information...")
        fleet = self.api.get_airline_fleet("TK")
        
        if not fleet:
            print("No A321neo aircraft found in fleet or API error occurred")
            return []
        
        all_flights = []
        
        for i, aircraft in enumerate(fleet, 1):
            registration = aircraft.get("registration", "")
            print(f"Processing aircraft {i}/{len(fleet)}: {registration}")
            
            flights = self.api.get_aircraft_flights(registration, days_back)
            all_flights.extend(flights)
            
            # Rate limiting - wait between requests
            time.sleep(1)
        
        self.all_flights = all_flights
        print(f"Total flights retrieved: {len(all_flights)}")
        return all_flights
    
    def export_to_csv(self, filename: str = "turkish_airlines_a321neo_flights.csv"):
        """Export flight data to CSV file"""
        if not self.all_flights:
            print("No flight data to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'registration', 'flight_number', 'departure_airport', 
                'arrival_airport', 'departure_time', 'arrival_time', 
                'flight_duration', 'aircraft_type', 'status', 'date'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for flight in self.all_flights:
                writer.writerow(asdict(flight))
        
        print(f"Flight data exported to {filename}")
    
    def export_to_json(self, filename: str = "turkish_airlines_a321neo_flights.json"):
        """Export flight data to JSON file"""
        if not self.all_flights:
            print("No flight data to export")
            return
        
        flight_dicts = [asdict(flight) for flight in self.all_flights]
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(flight_dicts, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Flight data exported to {filename}")
    
    def print_summary(self):
        """Print summary statistics of the flight data"""
        if not self.all_flights:
            print("No flight data available")
            return
        
        # Group by aircraft
        aircraft_flights = {}
        for flight in self.all_flights:
            reg = flight.registration
            if reg not in aircraft_flights:
                aircraft_flights[reg] = []
            aircraft_flights[reg].append(flight)
        
        print("\n" + "="*60)
        print("TURKISH AIRLINES A321NEO FLEET SUMMARY")
        print("="*60)
        print(f"Total Aircraft: {len(aircraft_flights)}")
        print(f"Total Flights: {len(self.all_flights)}")
        
        print("\nFlights per Aircraft:")
        for reg, flights in sorted(aircraft_flights.items()):
            total_duration = sum(
                self._parse_duration(flight.flight_duration) 
                for flight in flights 
                if flight.flight_duration
            )
            avg_duration = total_duration / len(flights) if flights else 0
            
            print(f"  {reg}: {len(flights)} flights, "
                  f"Avg Duration: {avg_duration:.1f} hours")
        
        # Route analysis
        routes = {}
        for flight in self.all_flights:
            route = f"{flight.departure_airport}-{flight.arrival_airport}"
            routes[route] = routes.get(route, 0) + 1
        
        print(f"\nTop 10 Routes:")
        for route, count in sorted(routes.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {route}: {count} flights")
    
    def _parse_duration(self, duration_str: str) -> float:
        """Parse duration string (HH:MM) to hours as float"""
        if not duration_str or ':' not in duration_str:
            return 0.0
        
        try:
            hours, minutes = map(int, duration_str.split(':'))
            return hours + minutes / 60.0
        except ValueError:
            return 0.0


def main():
    """Main function to run the fleet tracker"""
    # Get API key from environment variable or prompt user
    api_key = os.getenv('FLIGHTRADAR24_API_KEY')
    
    if not api_key:
        print("Please set your FlightRadar24 API key:")
        print("1. As environment variable: export FLIGHTRADAR24_API_KEY='your_api_key'")
        print("2. Or enter it when prompted below:")
        api_key = input("Enter your FlightRadar24 API key: ").strip()
    
    if not api_key:
        print("API key is required to use this script")
        return
    
    # Initialize tracker
    tracker = TurkishAirlinesFleetTracker(api_key)
    
    # Get user preferences
    try:
        days_back = int(input("Enter number of days to look back (default 30): ") or "30")
    except ValueError:
        days_back = 30
    
    print(f"\nFetching flight data for the last {days_back} days...")
    
    # Fetch fleet data
    flights = tracker.fetch_fleet_data(days_back)
    
    if flights:
        # Print summary
        tracker.print_summary()
        
        # Export data
        print("\nExporting data...")
        tracker.export_to_csv()
        tracker.export_to_json()
        
        print("\nData collection complete!")
        print("Files created:")
        print("- turkish_airlines_a321neo_flights.csv")
        print("- turkish_airlines_a321neo_flights.json")
    else:
        print("No flight data was retrieved. Please check your API key and try again.")


if __name__ == "__main__":
    main()