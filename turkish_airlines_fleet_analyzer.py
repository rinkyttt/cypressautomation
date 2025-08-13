#!/usr/bin/env python3
"""
Turkish Airlines Fleet Analyzer
Fetches flight data for ALL Turkish Airlines aircraft using FlightRadar24 API
Provides detailed statistics per aircraft registration including total flight time and flight count
"""

import requests
import json
import csv
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import os
from dataclasses import dataclass, asdict
from collections import defaultdict


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
    duration_minutes: int = 0


@dataclass
class AircraftStats:
    """Statistics for a single aircraft"""
    registration: str
    aircraft_type: str
    total_flights: int
    total_flight_time_minutes: int
    total_flight_time_hours: float
    average_flight_time_minutes: float
    first_flight_date: str
    last_flight_date: str
    unique_routes: int
    most_common_route: str
    most_common_route_count: int


class FlightRadar24API:
    """FlightRadar24 API client for fetching aircraft and flight data"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.flightradar24.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Turkish-Airlines-Fleet-Analyzer/1.0"
        }
        
    def get_airline_fleet(self, airline_code: str = "TK") -> List[Dict]:
        """
        Retrieve fleet information for Turkish Airlines (ALL aircraft types)
        
        Args:
            airline_code: IATA code for Turkish Airlines (TK)
            
        Returns:
            List of all aircraft in the fleet
        """
        url = f"{self.base_url}/common/v1/airline/fleet.json"
        params = {"airline": airline_code}
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            fleet = data.get("aircraft", [])
            
            # Group by aircraft type for summary
            type_counts = defaultdict(int)
            for aircraft in fleet:
                aircraft_type = aircraft.get("type", "Unknown")
                type_counts[aircraft_type] += 1
            
            print(f"Found {len(fleet)} aircraft in Turkish Airlines fleet")
            print("Aircraft types in fleet:")
            for aircraft_type, count in sorted(type_counts.items()):
                print(f"  {aircraft_type}: {count} aircraft")
            
            return fleet
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching fleet data: {e}")
            return []
    
    def get_aircraft_flights(self, registration: str, aircraft_type: str, days_back: int = 365) -> List[FlightData]:
        """
        Retrieve flight history for a specific aircraft
        
        Args:
            registration: Aircraft registration number (e.g., TC-LTI)
            aircraft_type: Aircraft type code (e.g., A21N, B77W)
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
                departure_ts = flight.get("time_scheduled_departure")
                arrival_ts = flight.get("time_scheduled_arrival")
                duration_minutes = self._calculate_duration_minutes(departure_ts, arrival_ts)
                
                flight_data = FlightData(
                    registration=registration,
                    flight_number=flight.get("flight", ""),
                    departure_airport=flight.get("airport_origin", {}).get("iata", ""),
                    arrival_airport=flight.get("airport_destination", {}).get("iata", ""),
                    departure_time=self._format_timestamp(departure_ts),
                    arrival_time=self._format_timestamp(arrival_ts),
                    flight_duration=self._format_duration(duration_minutes),
                    aircraft_type=aircraft_type,
                    status=flight.get("status", ""),
                    date=self._format_date(departure_ts),
                    duration_minutes=duration_minutes
                )
                flights.append(flight_data)
                
            print(f"Retrieved {len(flights)} flights for {aircraft_type} {registration}")
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
    
    def _calculate_duration_minutes(self, departure: Optional[int], arrival: Optional[int]) -> int:
        """Calculate flight duration in minutes from departure and arrival timestamps"""
        if not departure or not arrival:
            return 0
        
        duration_seconds = arrival - departure
        return max(0, duration_seconds // 60)  # Convert to minutes
    
    def _format_duration(self, minutes: int) -> str:
        """Format duration from minutes to HH:MM format"""
        if minutes <= 0:
            return ""
        
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"


class TurkishAirlinesFleetAnalyzer:
    """Main class for analyzing Turkish Airlines entire fleet"""
    
    def __init__(self, api_key: str):
        self.api = FlightRadar24API(api_key)
        self.all_flights = []
        self.aircraft_stats = {}
        
    def analyze_fleet(self, days_back: int = 365) -> Dict[str, AircraftStats]:
        """
        Analyze entire Turkish Airlines fleet
        
        Args:
            days_back: Number of days to look back for flight history
            
        Returns:
            Dictionary of aircraft statistics by registration
        """
        print(f"Analyzing Turkish Airlines fleet for the past {days_back} days...")
        fleet = self.api.get_airline_fleet("TK")
        
        if not fleet:
            print("No aircraft found in fleet or API error occurred")
            return {}
        
        all_flights = []
        aircraft_stats = {}
        
        for i, aircraft in enumerate(fleet, 1):
            registration = aircraft.get("registration", "")
            aircraft_type = aircraft.get("type", "Unknown")
            
            print(f"Processing aircraft {i}/{len(fleet)}: {aircraft_type} {registration}")
            
            flights = self.api.get_aircraft_flights(registration, aircraft_type, days_back)
            all_flights.extend(flights)
            
            # Calculate statistics for this aircraft
            if flights:
                stats = self._calculate_aircraft_stats(registration, aircraft_type, flights)
                aircraft_stats[registration] = stats
            else:
                # Create empty stats for aircraft with no flights
                aircraft_stats[registration] = AircraftStats(
                    registration=registration,
                    aircraft_type=aircraft_type,
                    total_flights=0,
                    total_flight_time_minutes=0,
                    total_flight_time_hours=0.0,
                    average_flight_time_minutes=0.0,
                    first_flight_date="",
                    last_flight_date="",
                    unique_routes=0,
                    most_common_route="",
                    most_common_route_count=0
                )
            
            # Rate limiting - wait between requests
            time.sleep(1)
        
        self.all_flights = all_flights
        self.aircraft_stats = aircraft_stats
        
        print(f"\nAnalysis complete!")
        print(f"Total aircraft analyzed: {len(aircraft_stats)}")
        print(f"Total flights retrieved: {len(all_flights)}")
        
        return aircraft_stats
    
    def _calculate_aircraft_stats(self, registration: str, aircraft_type: str, flights: List[FlightData]) -> AircraftStats:
        """Calculate comprehensive statistics for a single aircraft"""
        if not flights:
            return AircraftStats(
                registration=registration,
                aircraft_type=aircraft_type,
                total_flights=0,
                total_flight_time_minutes=0,
                total_flight_time_hours=0.0,
                average_flight_time_minutes=0.0,
                first_flight_date="",
                last_flight_date="",
                unique_routes=0,
                most_common_route="",
                most_common_route_count=0
            )
        
        # Calculate flight time statistics
        total_minutes = sum(flight.duration_minutes for flight in flights)
        total_hours = total_minutes / 60.0
        avg_minutes = total_minutes / len(flights) if flights else 0
        
        # Find date range
        dates = [flight.date for flight in flights if flight.date]
        first_date = min(dates) if dates else ""
        last_date = max(dates) if dates else ""
        
        # Analyze routes
        routes = defaultdict(int)
        for flight in flights:
            if flight.departure_airport and flight.arrival_airport:
                route = f"{flight.departure_airport}-{flight.arrival_airport}"
                routes[route] += 1
        
        most_common_route = ""
        most_common_count = 0
        if routes:
            most_common_route, most_common_count = max(routes.items(), key=lambda x: x[1])
        
        return AircraftStats(
            registration=registration,
            aircraft_type=aircraft_type,
            total_flights=len(flights),
            total_flight_time_minutes=total_minutes,
            total_flight_time_hours=total_hours,
            average_flight_time_minutes=avg_minutes,
            first_flight_date=first_date,
            last_flight_date=last_date,
            unique_routes=len(routes),
            most_common_route=most_common_route,
            most_common_route_count=most_common_count
        )
    
    def export_aircraft_stats_to_csv(self, filename: str = "turkish_airlines_aircraft_stats.csv"):
        """Export aircraft statistics to CSV file"""
        if not self.aircraft_stats:
            print("No aircraft statistics to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'registration', 'aircraft_type', 'total_flights', 
                'total_flight_time_hours', 'total_flight_time_minutes',
                'average_flight_time_minutes', 'first_flight_date', 
                'last_flight_date', 'unique_routes', 'most_common_route',
                'most_common_route_count'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for stats in self.aircraft_stats.values():
                writer.writerow(asdict(stats))
        
        print(f"Aircraft statistics exported to {filename}")
    
    def export_flights_to_csv(self, filename: str = "turkish_airlines_all_flights.csv"):
        """Export all flight data to CSV file"""
        if not self.all_flights:
            print("No flight data to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'registration', 'aircraft_type', 'flight_number', 
                'departure_airport', 'arrival_airport', 'departure_time', 
                'arrival_time', 'flight_duration', 'duration_minutes',
                'status', 'date'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for flight in self.all_flights:
                writer.writerow(asdict(flight))
        
        print(f"Flight data exported to {filename}")
    
    def export_to_json(self, stats_filename: str = "aircraft_stats.json", flights_filename: str = "all_flights.json"):
        """Export data to JSON files"""
        if self.aircraft_stats:
            stats_dicts = {reg: asdict(stats) for reg, stats in self.aircraft_stats.items()}
            with open(stats_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(stats_dicts, jsonfile, indent=2, ensure_ascii=False)
            print(f"Aircraft statistics exported to {stats_filename}")
        
        if self.all_flights:
            flight_dicts = [asdict(flight) for flight in self.all_flights]
            with open(flights_filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(flight_dicts, jsonfile, indent=2, ensure_ascii=False)
            print(f"Flight data exported to {flights_filename}")
    
    def print_detailed_summary(self):
        """Print comprehensive fleet analysis summary"""
        if not self.aircraft_stats:
            print("No aircraft statistics available")
            return
        
        print("\n" + "="*80)
        print("TURKISH AIRLINES FLEET ANALYSIS - DETAILED SUMMARY")
        print("="*80)
        
        # Overall fleet statistics
        total_aircraft = len(self.aircraft_stats)
        active_aircraft = len([s for s in self.aircraft_stats.values() if s.total_flights > 0])
        total_flights = sum(stats.total_flights for stats in self.aircraft_stats.values())
        total_flight_hours = sum(stats.total_flight_time_hours for stats in self.aircraft_stats.values())
        
        print(f"Total Aircraft in Fleet: {total_aircraft}")
        print(f"Active Aircraft (with flights): {active_aircraft}")
        print(f"Total Flights: {total_flights:,}")
        print(f"Total Flight Hours: {total_flight_hours:,.1f}")
        print(f"Average Flight Hours per Aircraft: {total_flight_hours/active_aircraft:.1f}" if active_aircraft > 0 else "N/A")
        
        # Aircraft type breakdown
        print(f"\n{'AIRCRAFT TYPE SUMMARY':^80}")
        print("-" * 80)
        type_stats = defaultdict(lambda: {'count': 0, 'flights': 0, 'hours': 0})
        
        for stats in self.aircraft_stats.values():
            aircraft_type = stats.aircraft_type
            type_stats[aircraft_type]['count'] += 1
            type_stats[aircraft_type]['flights'] += stats.total_flights
            type_stats[aircraft_type]['hours'] += stats.total_flight_time_hours
        
        print(f"{'Type':<8} {'Count':<6} {'Flights':<8} {'Hours':<10} {'Avg Hours/Aircraft':<15}")
        print("-" * 80)
        for aircraft_type, data in sorted(type_stats.items()):
            avg_hours = data['hours'] / data['count'] if data['count'] > 0 else 0
            print(f"{aircraft_type:<8} {data['count']:<6} {data['flights']:<8} {data['hours']:<10.1f} {avg_hours:<15.1f}")
        
        # Top performers
        print(f"\n{'TOP PERFORMING AIRCRAFT':^80}")
        print("-" * 80)
        
        # Most flights
        most_flights = sorted(self.aircraft_stats.values(), key=lambda x: x.total_flights, reverse=True)[:10]
        print(f"\nTop 10 by Flight Count:")
        print(f"{'Registration':<12} {'Type':<8} {'Flights':<8} {'Hours':<10} {'Avg/Flight':<10}")
        print("-" * 60)
        for stats in most_flights:
            avg_flight = stats.average_flight_time_minutes / 60 if stats.average_flight_time_minutes > 0 else 0
            print(f"{stats.registration:<12} {stats.aircraft_type:<8} {stats.total_flights:<8} "
                  f"{stats.total_flight_time_hours:<10.1f} {avg_flight:<10.1f}")
        
        # Most flight hours
        most_hours = sorted(self.aircraft_stats.values(), key=lambda x: x.total_flight_time_hours, reverse=True)[:10]
        print(f"\nTop 10 by Flight Hours:")
        print(f"{'Registration':<12} {'Type':<8} {'Hours':<10} {'Flights':<8} {'Routes':<8}")
        print("-" * 60)
        for stats in most_hours:
            print(f"{stats.registration:<12} {stats.aircraft_type:<8} {stats.total_flight_time_hours:<10.1f} "
                  f"{stats.total_flights:<8} {stats.unique_routes:<8}")
        
        # Detailed per-aircraft breakdown
        print(f"\n{'DETAILED AIRCRAFT BREAKDOWN':^80}")
        print("-" * 80)
        print(f"{'Registration':<12} {'Type':<8} {'Flights':<8} {'Hours':<10} {'Routes':<8} {'Top Route':<15}")
        print("-" * 80)
        
        for registration in sorted(self.aircraft_stats.keys()):
            stats = self.aircraft_stats[registration]
            top_route = stats.most_common_route[:14] if stats.most_common_route else "None"
            print(f"{stats.registration:<12} {stats.aircraft_type:<8} {stats.total_flights:<8} "
                  f"{stats.total_flight_time_hours:<10.1f} {stats.unique_routes:<8} {top_route:<15}")


def main():
    """Main function to run the fleet analyzer"""
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
    
    # Initialize analyzer
    analyzer = TurkishAirlinesFleetAnalyzer(api_key)
    
    # Get user preferences
    try:
        days_back = int(input("Enter number of days to look back (default 365): ") or "365")
    except ValueError:
        days_back = 365
    
    print(f"\nAnalyzing Turkish Airlines fleet for the last {days_back} days...")
    print("This may take a while as we're processing the entire fleet...")
    
    # Analyze fleet
    aircraft_stats = analyzer.analyze_fleet(days_back)
    
    if aircraft_stats:
        # Print detailed summary
        analyzer.print_detailed_summary()
        
        # Export data
        print(f"\n{'EXPORTING DATA':^80}")
        print("-" * 80)
        analyzer.export_aircraft_stats_to_csv()
        analyzer.export_flights_to_csv()
        analyzer.export_to_json()
        
        print("\nFleet analysis complete!")
        print("Files created:")
        print("- turkish_airlines_aircraft_stats.csv (per-aircraft statistics)")
        print("- turkish_airlines_all_flights.csv (all flight records)")
        print("- aircraft_stats.json (statistics in JSON format)")
        print("- all_flights.json (flight records in JSON format)")
    else:
        print("No fleet data was retrieved. Please check your API key and try again.")


if __name__ == "__main__":
    main()