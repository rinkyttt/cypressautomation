#!/usr/bin/env python3
"""
Flightradar24 API Usage Examples
===============================

Comprehensive examples demonstrating how to use the FR24 API client
for various flight tracking and aviation data tasks.
"""

from flightradar24_api_client import FlightRadar24Client, FR24DataCollector
import time
from datetime import datetime, timedelta

def example_1_live_flights():
    """Example 1: Get live flights in different regions"""
    print("🌍 EXAMPLE 1: Live Flights by Region")
    print("-" * 50)
    
    client = FlightRadar24Client()
    
    # Define popular regions
    regions = {
        "New York Area": {
            'north': 41.0, 'south': 40.0,
            'east': -73.0, 'west': -75.0
        },
        "London Area": {
            'north': 52.0, 'south': 51.0,
            'east': 1.0, 'west': -1.0
        },
        "Tokyo Area": {
            'north': 36.0, 'south': 35.0,
            'east': 140.5, 'west': 139.0
        }
    }
    
    for region_name, bounds in regions.items():
        print(f"\n📍 Getting flights for {region_name}...")
        
        try:
            flights = client.get_live_flights(bounds=bounds)
            
            if flights:
                print(f"✅ Found {len(flights)} flights in {region_name}")
                
                # Show sample flights
                print(f"   📋 Sample flights:")
                for i, flight in enumerate(flights[:3]):
                    callsign = flight.get('callsign', 'N/A')
                    origin = flight.get('origin', {}).get('iata', 'N/A')
                    destination = flight.get('destination', {}).get('iata', 'N/A')
                    print(f"      {i+1}. {callsign}: {origin} → {destination}")
                
                # Export regional data
                filename = f"{region_name.lower().replace(' ', '_')}_flights.json"
                client.export_to_json(flights, filename)
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error getting {region_name} flights: {e}")

def example_2_airport_operations():
    """Example 2: Monitor airport operations"""
    print("\n🏢 EXAMPLE 2: Airport Operations Monitoring")
    print("-" * 50)
    
    collector = FR24DataCollector()
    
    # Major airports to monitor
    airports = ['JFK', 'LAX', 'LHR', 'CDG', 'NRT', 'DXB']
    
    for airport in airports:
        print(f"\n🛫 Monitoring {airport}...")
        
        try:
            # Get comprehensive airport data
            airport_data = collector.collect_airport_data(airport)
            
            arrivals = len(airport_data['arrivals'])
            departures = len(airport_data['departures'])
            total_flights = arrivals + departures
            
            print(f"✅ {airport} Operations:")
            print(f"   📥 Arrivals: {arrivals}")
            print(f"   📤 Departures: {departures}")
            print(f"   📊 Total: {total_flights}")
            
            # Find busiest routes
            routes = {}
            for flight in airport_data['departures']:
                dest = flight.get('destination', {}).get('iata', 'Unknown')
                routes[dest] = routes.get(dest, 0) + 1
            
            if routes:
                top_routes = sorted(routes.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   🔥 Top destinations:")
                for dest, count in top_routes:
                    print(f"      {dest}: {count} flights")
            
            # Export airport data
            client = FlightRadar24Client()
            client.export_to_json(airport_data, f"{airport.lower()}_operations.json")
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error monitoring {airport}: {e}")

def example_3_airline_analysis():
    """Example 3: Airline fleet and operations analysis"""
    print("\n✈️ EXAMPLE 3: Airline Analysis")
    print("-" * 50)
    
    collector = FR24DataCollector()
    
    # Major airlines to analyze
    airlines = ['AA', 'DL', 'UA', 'BA', 'LH', 'AF']
    
    for airline in airlines:
        print(f"\n🏢 Analyzing {airline}...")
        
        try:
            # Get comprehensive airline data
            airline_data = collector.collect_airline_data(airline)
            
            fleet_size = len(airline_data['fleet'])
            airline_info = airline_data['airline_info']
            
            print(f"✅ {airline} Analysis:")
            print(f"   🛩️  Fleet size: {fleet_size} aircraft")
            print(f"   🏢 Name: {airline_info.get('name', 'N/A')}")
            
            # Analyze fleet composition
            aircraft_types = {}
            for aircraft in airline_data['fleet']:
                model = aircraft.get('aircraft', {}).get('model', 'Unknown')
                aircraft_types[model] = aircraft_types.get(model, 0) + 1
            
            if aircraft_types:
                top_types = sorted(aircraft_types.items(), key=lambda x: x[1], reverse=True)[:3]
                print(f"   📋 Top aircraft types:")
                for aircraft_type, count in top_types:
                    print(f"      {aircraft_type}: {count} aircraft")
            
            # Export airline data
            client = FlightRadar24Client()
            client.export_to_json(airline_data, f"{airline.lower()}_analysis.json")
            
            # Rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error analyzing {airline}: {e}")

def example_4_flight_tracking():
    """Example 4: Track specific flights"""
    print("\n🎯 EXAMPLE 4: Flight Tracking")
    print("-" * 50)
    
    client = FlightRadar24Client()
    
    # Search for flights
    search_queries = ['AA100', 'BA1', 'LH400', 'AF447']
    
    for query in search_queries:
        print(f"\n🔍 Searching for flight: {query}")
        
        try:
            # Search for the flight
            search_results = client.search_flights(query, limit=5)
            
            if search_results:
                print(f"✅ Found {len(search_results)} results for {query}")
                
                for i, flight in enumerate(search_results[:2]):
                    flight_id = flight.get('id')
                    callsign = flight.get('callsign', 'N/A')
                    
                    print(f"   📋 Result {i+1}: {callsign} (ID: {flight_id})")
                    
                    if flight_id:
                        # Get detailed flight information
                        try:
                            details = client.get_flight_details(flight_id)
                            
                            origin = details.get('origin', {}).get('iata', 'N/A')
                            destination = details.get('destination', {}).get('iata', 'N/A')
                            status = details.get('status', 'N/A')
                            
                            print(f"      Route: {origin} → {destination}")
                            print(f"      Status: {status}")
                            
                            # Get flight track
                            track = client.get_flight_track(flight_id)
                            track_points = track.get('data', [])
                            
                            if track_points:
                                print(f"      Track: {len(track_points)} position points")
                            
                        except Exception as e:
                            print(f"      ❌ Error getting details: {e}")
            else:
                print(f"❌ No results found for {query}")
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error searching for {query}: {e}")

def example_5_aircraft_info():
    """Example 5: Aircraft information lookup"""
    print("\n🛫 EXAMPLE 5: Aircraft Information")
    print("-" * 50)
    
    client = FlightRadar24Client()
    
    # Sample aircraft registrations (these may or may not exist)
    registrations = ['N12345', 'G-ABCD', 'D-EFGH', 'JA123A']
    
    for registration in registrations:
        print(f"\n🔍 Looking up aircraft: {registration}")
        
        try:
            aircraft_info = client.get_aircraft_info(registration)
            
            if aircraft_info:
                print(f"✅ Found aircraft {registration}:")
                print(f"   🛩️  Type: {aircraft_info.get('aircraft', {}).get('model', 'N/A')}")
                print(f"   🏢 Owner: {aircraft_info.get('owner', 'N/A')}")
                print(f"   📅 Age: {aircraft_info.get('age', 'N/A')} years")
                
                # Export aircraft data
                client.export_to_json(aircraft_info, f"aircraft_{registration.replace('-', '_')}.json")
            else:
                print(f"❌ No information found for {registration}")
            
            # Rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error looking up {registration}: {e}")

def example_6_data_analysis():
    """Example 6: Comprehensive data analysis"""
    print("\n📊 EXAMPLE 6: Data Analysis")
    print("-" * 50)
    
    client = FlightRadar24Client()
    
    # Get flights from a busy region (US East Coast)
    bounds = {
        'north': 45.0, 'south': 35.0,
        'east': -65.0, 'west': -85.0
    }
    
    print("📡 Getting flights for analysis...")
    
    try:
        flights = client.get_live_flights(bounds=bounds)
        
        if flights:
            print(f"✅ Retrieved {len(flights)} flights for analysis")
            
            # Generate comprehensive statistics
            stats = client.get_statistics(flights)
            
            print(f"\n📈 FLIGHT STATISTICS:")
            print(f"   Total flights: {stats['total_flights']}")
            
            print(f"\n🏢 Top Airlines:")
            for airline, count in list(stats['airlines'].items())[:5]:
                percentage = (count / stats['total_flights']) * 100
                print(f"   {airline}: {count} ({percentage:.1f}%)")
            
            print(f"\n✈️ Top Aircraft Types:")
            for aircraft, count in list(stats['aircraft_types'].items())[:5]:
                percentage = (count / stats['total_flights']) * 100
                print(f"   {aircraft}: {count} ({percentage:.1f}%)")
            
            print(f"\n🛫 Top Origin Airports:")
            for origin, count in list(stats['origins'].items())[:5]:
                percentage = (count / stats['total_flights']) * 100
                print(f"   {origin}: {count} ({percentage:.1f}%)")
            
            print(f"\n🛬 Top Destination Airports:")
            for dest, count in list(stats['destinations'].items())[:5]:
                percentage = (count / stats['total_flights']) * 100
                print(f"   {dest}: {count} ({percentage:.1f}%)")
            
            # Export comprehensive analysis
            analysis_data = {
                'flights': flights,
                'statistics': stats,
                'analysis_time': datetime.now().isoformat(),
                'region': 'US East Coast'
            }
            
            client.export_to_json(analysis_data, "comprehensive_analysis.json")
            client.export_flights_to_csv(flights, "flights_analysis.csv")
            
        else:
            print("❌ No flights retrieved for analysis")
    
    except Exception as e:
        print(f"❌ Error in data analysis: {e}")

def main():
    """Run all examples"""
    print("🛩️ FLIGHTRADAR24 API - COMPREHENSIVE EXAMPLES")
    print("=" * 60)
    
    try:
        # Test API connection first
        client = FlightRadar24Client()
        if not client.test_connection():
            print("❌ API connection failed. Please check your setup:")
            print("1. Ensure you have a valid FR24 API subscription")
            print("2. Set your API token: FR24_API_TOKEN=your_token")
            print("3. Check your internet connection")
            return
        
        print("✅ API connection successful! Running examples...\n")
        
        # Run all examples
        example_1_live_flights()
        
        time.sleep(3)
        example_2_airport_operations()
        
        time.sleep(3)
        example_3_airline_analysis()
        
        time.sleep(3)
        example_4_flight_tracking()
        
        time.sleep(3)
        example_5_aircraft_info()
        
        time.sleep(3)
        example_6_data_analysis()
        
        print(f"\n" + "=" * 60)
        print("✅ ALL EXAMPLES COMPLETED!")
        print("=" * 60)
        print("📁 Generated files:")
        print("   - Regional flight data (JSON)")
        print("   - Airport operations data (JSON)")
        print("   - Airline analysis data (JSON)")
        print("   - Aircraft information (JSON)")
        print("   - Comprehensive analysis (JSON + CSV)")
        print("\n🚀 Your FR24 API integration is working perfectly!")
        
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n💡 SETUP REQUIRED:")
        print("1. Subscribe to FR24 API: https://www.flightradar24.com/commercial-services/api")
        print("2. Get your API token from the dashboard")
        print("3. Set environment variable: FR24_API_TOKEN=your_token")
        print("4. Run this script again")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("Please check your API token and internet connection.")

if __name__ == "__main__":
    main()