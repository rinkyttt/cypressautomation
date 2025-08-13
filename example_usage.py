#!/usr/bin/env python3
"""
Flight Scraper Usage Examples
============================

This file demonstrates various ways to use the flight data scraper.
"""

from flight_scraper import FlightScraper, OpenSkyNetworkScraper
import time

def example_1_basic_usage():
    """Example 1: Basic flight data retrieval"""
    print("🚀 Example 1: Basic Flight Data Retrieval")
    print("-" * 50)
    
    # Initialize the scraper
    scraper = FlightScraper()
    
    # Get current flights worldwide
    flights = scraper.get_all_flights(use_opensky=True)
    
    if flights:
        print(f"Found {len(flights)} active flights worldwide")
        
        # Show some statistics
        countries = {}
        grounded = 0
        for flight in flights:
            countries[flight.origin_country] = countries.get(flight.origin_country, 0) + 1
            if flight.on_ground:
                grounded += 1
        
        print(f"Aircraft on ground: {grounded}")
        print(f"Top 5 countries by aircraft count:")
        for country, count in sorted(countries.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  {country}: {count}")
        
        # Export the data
        scraper.export_data(flights, 'json', 'worldwide_flights.json')
    
    print()

def example_2_regional_flights():
    """Example 2: Regional flight data"""
    print("🌍 Example 2: Regional Flight Data")
    print("-" * 50)
    
    scraper = FlightScraper()
    
    # Get flights for different regions
    regions = ['europe', 'usa', 'asia']
    
    for region in regions:
        print(f"\nFetching flights for {region.upper()}...")
        regional_flights = scraper.get_flights_by_region(region)
        
        if regional_flights:
            print(f"Found {len(regional_flights)} flights in {region}")
            
            # Find the highest flying aircraft
            highest_flight = max(
                (f for f in regional_flights if f.baro_altitude), 
                key=lambda x: x.baro_altitude or 0,
                default=None
            )
            
            if highest_flight:
                altitude_ft = (highest_flight.baro_altitude or 0) * 3.28084  # Convert to feet
                print(f"Highest aircraft: {highest_flight.callsign or 'Unknown'} at {altitude_ft:.0f} ft")
            
            # Export regional data
            scraper.export_data(regional_flights, 'csv', f'{region}_flights.csv')
        
        # Be nice to the API
        time.sleep(2)
    
    print()

def example_3_specific_aircraft():
    """Example 3: Track specific aircraft"""
    print("✈️ Example 3: Track Specific Aircraft")
    print("-" * 50)
    
    # Create OpenSky scraper directly for more control
    opensky = OpenSkyNetworkScraper()
    
    # Example ICAO24 codes (these might not always be active)
    aircraft_codes = ['a0a0a0', 'b0b0b0', 'c0c0c0']  # Replace with real codes
    
    for icao24 in aircraft_codes:
        print(f"\nLooking for aircraft {icao24}...")
        flights = opensky.get_states(icao24=icao24)
        
        if flights:
            flight = flights[0]
            print(f"✓ Found: {flight.callsign or 'Unknown callsign'}")
            if flight.latitude and flight.longitude:
                print(f"  Position: {flight.latitude:.4f}, {flight.longitude:.4f}")
            if flight.baro_altitude:
                print(f"  Altitude: {flight.baro_altitude:.0f} m")
            print(f"  Country: {flight.origin_country}")
        else:
            print("  Aircraft not found or not active")
        
        time.sleep(1)
    
    print()

def example_4_custom_bounding_box():
    """Example 4: Custom geographic area"""
    print("📍 Example 4: Custom Geographic Area")
    print("-" * 50)
    
    opensky = OpenSkyNetworkScraper()
    
    # Define a custom bounding box (example: around London)
    london_bbox = {
        'min_lat': 51.0,   # South
        'max_lat': 52.0,   # North  
        'min_lon': -1.0,   # West
        'max_lon': 1.0     # East
    }
    
    print("Searching for flights around London...")
    london_flights = opensky.get_flights_by_bbox(
        london_bbox['min_lat'], london_bbox['min_lon'],
        london_bbox['max_lat'], london_bbox['max_lon']
    )
    
    if london_flights:
        print(f"Found {len(london_flights)} flights around London")
        
        # Show some details
        for i, flight in enumerate(london_flights[:5]):  # Show first 5
            print(f"{i+1}. {flight.callsign or 'N/A'} from {flight.origin_country}")
            if flight.latitude and flight.longitude:
                print(f"   Position: {flight.latitude:.4f}, {flight.longitude:.4f}")
        
        # Export London area flights
        scraper = FlightScraper()
        scraper.export_data(london_flights, 'json', 'london_area_flights.json')
    
    print()

def example_5_data_analysis():
    """Example 5: Basic data analysis"""
    print("📊 Example 5: Basic Data Analysis")
    print("-" * 50)
    
    scraper = FlightScraper()
    flights = scraper.get_all_flights(use_opensky=True)
    
    if not flights:
        print("No flight data available for analysis")
        return
    
    # Basic statistics
    total_flights = len(flights)
    grounded_flights = sum(1 for f in flights if f.on_ground)
    airborne_flights = total_flights - grounded_flights
    
    print(f"Total flights: {total_flights}")
    print(f"Airborne: {airborne_flights}")
    print(f"On ground: {grounded_flights}")
    
    # Altitude analysis (for airborne flights)
    airborne_with_altitude = [f for f in flights if not f.on_ground and f.baro_altitude]
    
    if airborne_with_altitude:
        altitudes = [f.baro_altitude for f in airborne_with_altitude]
        avg_altitude = sum(altitudes) / len(altitudes)
        max_altitude = max(altitudes)
        min_altitude = min(altitudes)
        
        print(f"\nAltitude Analysis ({len(airborne_with_altitude)} flights):")
        print(f"Average altitude: {avg_altitude:.0f} m ({avg_altitude * 3.28084:.0f} ft)")
        print(f"Maximum altitude: {max_altitude:.0f} m ({max_altitude * 3.28084:.0f} ft)")
        print(f"Minimum altitude: {min_altitude:.0f} m ({min_altitude * 3.28084:.0f} ft)")
    
    # Speed analysis
    flights_with_speed = [f for f in flights if f.velocity is not None]
    if flights_with_speed:
        speeds = [f.velocity for f in flights_with_speed]
        avg_speed = sum(speeds) / len(speeds)
        max_speed = max(speeds)
        
        print(f"\nSpeed Analysis ({len(flights_with_speed)} flights):")
        print(f"Average speed: {avg_speed:.1f} m/s ({avg_speed * 3.6:.1f} km/h)")
        print(f"Maximum speed: {max_speed:.1f} m/s ({max_speed * 3.6:.1f} km/h)")
    
    # Country distribution
    country_counts = {}
    for flight in flights:
        country = flight.origin_country
        country_counts[country] = country_counts.get(country, 0) + 1
    
    print(f"\nTop 10 Countries by Aircraft Count:")
    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        percentage = (count / total_flights) * 100
        print(f"{country}: {count} ({percentage:.1f}%)")
    
    print()

def main():
    """Run all examples"""
    print("🛩️ Flight Data Scraper - Usage Examples")
    print("=" * 60)
    print()
    
    try:
        # Run examples with delays between them
        example_1_basic_usage()
        time.sleep(3)
        
        example_2_regional_flights()
        time.sleep(3)
        
        example_3_specific_aircraft()
        time.sleep(3)
        
        example_4_custom_bounding_box()
        time.sleep(3)
        
        example_5_data_analysis()
        
    except KeyboardInterrupt:
        print("\n⚠ Interrupted by user")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("✅ Examples completed!")
    print("\nGenerated files:")
    print("- worldwide_flights.json")
    print("- europe_flights.csv") 
    print("- usa_flights.csv")
    print("- asia_flights.csv")
    print("- london_area_flights.json")

if __name__ == "__main__":
    main()