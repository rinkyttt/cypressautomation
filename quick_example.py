#!/usr/bin/env python3
"""
Quick Example: Turkish Airlines Fleet Analyzer
Demonstrates usage with a smaller time window for faster testing
"""

import os
from turkish_airlines_fleet_analyzer import TurkishAirlinesFleetAnalyzer

def main():
    """Quick example with 7 days of data"""
    
    # You can set your API key here or use environment variable
    api_key = os.getenv('FLIGHTRADAR24_API_KEY')
    
    if not api_key:
        # Replace with your actual API key for testing
        api_key = "YOUR_API_KEY_HERE"
    
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Please set FLIGHTRADAR24_API_KEY environment variable or edit this script")
        return
    
    print("=== TURKISH AIRLINES FLEET ANALYZER - QUICK DEMO ===")
    print("Analyzing fleet for the past 7 days (for faster testing)...")
    
    # Initialize analyzer
    analyzer = TurkishAirlinesFleetAnalyzer(api_key)
    
    # Analyze fleet for past 7 days (faster for testing)
    aircraft_stats = analyzer.analyze_fleet(days_back=7)
    
    if aircraft_stats:
        # Show summary
        analyzer.print_detailed_summary()
        
        # Export sample data
        print("\nExporting sample data...")
        analyzer.export_aircraft_stats_to_csv("sample_aircraft_stats.csv")
        analyzer.export_flights_to_csv("sample_all_flights.csv")
        
        # Show some specific examples
        print("\n" + "="*60)
        print("SAMPLE AIRCRAFT DETAILS")
        print("="*60)
        
        # Show first 5 aircraft with flights
        active_aircraft = [stats for stats in aircraft_stats.values() if stats.total_flights > 0]
        for i, stats in enumerate(active_aircraft[:5]):
            print(f"\n{i+1}. {stats.registration} ({stats.aircraft_type})")
            print(f"   Total Flights: {stats.total_flights}")
            print(f"   Total Flight Time: {stats.total_flight_time_hours:.1f} hours")
            print(f"   Average Flight Time: {stats.average_flight_time_minutes:.0f} minutes")
            print(f"   Unique Routes: {stats.unique_routes}")
            print(f"   Most Common Route: {stats.most_common_route} ({stats.most_common_route_count} times)")
        
        print(f"\nSample files created:")
        print("- sample_aircraft_stats.csv")
        print("- sample_all_flights.csv")
        
    else:
        print("No data retrieved. Check your API key.")

if __name__ == "__main__":
    main()