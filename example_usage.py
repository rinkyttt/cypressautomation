#!/usr/bin/env python3
"""
Example usage of Turkish Airlines A321neo Fleet Tracker
This script demonstrates how to use the tracker programmatically
"""

import os
from turkish_airlines_a321neo_tracker import TurkishAirlinesFleetTracker

def main():
    """Example of programmatic usage"""
    
    # Set your API key (replace with your actual key)
    api_key = "YOUR_FLIGHTRADAR24_API_KEY_HERE"
    
    # Or get from environment variable
    # api_key = os.getenv('FLIGHTRADAR24_API_KEY')
    
    if not api_key or api_key == "YOUR_FLIGHTRADAR24_API_KEY_HERE":
        print("Please set your actual FlightRadar24 API key in this script or as environment variable")
        return
    
    # Initialize the tracker
    print("Initializing Turkish Airlines A321neo Fleet Tracker...")
    tracker = TurkishAirlinesFleetTracker(api_key)
    
    # Fetch data for the last 7 days
    print("Fetching flight data for the last 7 days...")
    flights = tracker.fetch_fleet_data(days_back=7)
    
    if not flights:
        print("No flight data retrieved. Check your API key and try again.")
        return
    
    # Print summary
    tracker.print_summary()
    
    # Export to files
    print("\nExporting data to files...")
    tracker.export_to_csv("example_flights.csv")
    tracker.export_to_json("example_flights.json")
    
    # Example: Analyze specific data
    print("\n" + "="*50)
    print("CUSTOM ANALYSIS EXAMPLE")
    print("="*50)
    
    # Group flights by aircraft registration
    aircraft_stats = {}
    for flight in flights:
        reg = flight.registration
        if reg not in aircraft_stats:
            aircraft_stats[reg] = {
                'flights': 0,
                'routes': set(),
                'total_duration': 0
            }
        
        aircraft_stats[reg]['flights'] += 1
        aircraft_stats[reg]['routes'].add(f"{flight.departure_airport}-{flight.arrival_airport}")
        
        # Parse duration
        if flight.flight_duration and ':' in flight.flight_duration:
            try:
                hours, minutes = map(int, flight.flight_duration.split(':'))
                aircraft_stats[reg]['total_duration'] += hours + minutes / 60.0
            except ValueError:
                pass
    
    # Find most active aircraft
    most_active = max(aircraft_stats.items(), key=lambda x: x[1]['flights'])
    print(f"Most active aircraft: {most_active[0]} with {most_active[1]['flights']} flights")
    
    # Find aircraft with most unique routes
    most_routes = max(aircraft_stats.items(), key=lambda x: len(x[1]['routes']))
    print(f"Aircraft with most routes: {most_routes[0]} with {len(most_routes[1]['routes'])} unique routes")
    
    # Calculate average flight duration across fleet
    total_flights = sum(stats['flights'] for stats in aircraft_stats.values())
    total_duration = sum(stats['total_duration'] for stats in aircraft_stats.values())
    avg_duration = total_duration / total_flights if total_flights > 0 else 0
    print(f"Average flight duration across fleet: {avg_duration:.1f} hours")
    
    # Example: Find specific routes
    ist_flights = [f for f in flights if f.departure_airport == "IST"]
    print(f"Flights departing from Istanbul (IST): {len(ist_flights)}")
    
    # Example: Group by date
    daily_flights = {}
    for flight in flights:
        date = flight.date
        if date not in daily_flights:
            daily_flights[date] = 0
        daily_flights[date] += 1
    
    print("\nDaily flight counts:")
    for date, count in sorted(daily_flights.items()):
        print(f"  {date}: {count} flights")
    
    print(f"\nExample analysis complete!")
    print("Check 'example_flights.csv' and 'example_flights.json' for exported data")

if __name__ == "__main__":
    main()