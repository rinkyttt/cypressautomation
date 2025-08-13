#!/usr/bin/env python3
"""
Quick 30-Day Fleet Analysis with Excel Export
Turkish Airlines Fleet Analyzer - 30 days with Excel output
"""

import os
from turkish_airlines_fleet_analyzer import TurkishAirlinesFleetAnalyzer

def main():
    """30-day analysis with Excel export"""
    
    # Get API key
    api_key = os.getenv('FLIGHTRADAR24_API_KEY')
    
    if not api_key:
        print("Please set your FlightRadar24 API key:")
        print("export FLIGHTRADAR24_API_KEY='your_api_key_here'")
        print("Or enter it below:")
        api_key = input("Enter your FlightRadar24 API key: ").strip()
    
    if not api_key:
        print("API key is required")
        return
    
    print("=" * 70)
    print("TURKISH AIRLINES FLEET ANALYZER - 30 DAY ANALYSIS")
    print("=" * 70)
    print("Analyzing Turkish Airlines fleet for the past 30 days...")
    print("This will include Excel export with multiple worksheets")
    print()
    
    # Initialize analyzer
    analyzer = TurkishAirlinesFleetAnalyzer(api_key)
    
    # Analyze fleet for past 30 days
    aircraft_stats = analyzer.analyze_fleet(days_back=30)
    
    if aircraft_stats:
        # Show summary
        analyzer.print_detailed_summary()
        
        # Export all formats including Excel
        print("\n" + "=" * 70)
        print("EXPORTING DATA TO MULTIPLE FORMATS")
        print("=" * 70)
        
        analyzer.export_aircraft_stats_to_csv("30day_aircraft_stats.csv")
        analyzer.export_flights_to_csv("30day_all_flights.csv")
        analyzer.export_to_json("30day_aircraft_stats.json", "30day_all_flights.json")
        analyzer.export_to_excel("turkish_airlines_30day_analysis.xlsx")
        
        print("\n✅ 30-Day Analysis Complete!")
        print("\nFiles created:")
        print("📊 turkish_airlines_30day_analysis.xlsx (MAIN EXCEL FILE)")
        print("   └── Aircraft Statistics (sorted by flight hours)")
        print("   └── Aircraft Type Summary (breakdown by type)")
        print("   └── Top Performers (rankings)")
        print("   └── All Flights (individual flight records)")
        print()
        print("📄 CSV Files:")
        print("   └── 30day_aircraft_stats.csv")
        print("   └── 30day_all_flights.csv")
        print()
        print("📄 JSON Files:")
        print("   └── 30day_aircraft_stats.json")
        print("   └── 30day_all_flights.json")
        
        # Show quick stats
        active_aircraft = len([s for s in aircraft_stats.values() if s.total_flights > 0])
        total_flights = sum(s.total_flights for s in aircraft_stats.values())
        total_hours = sum(s.total_flight_time_hours for s in aircraft_stats.values())
        
        print("\n📈 QUICK STATS (30 days):")
        print(f"   Total Aircraft: {len(aircraft_stats)}")
        print(f"   Active Aircraft: {active_aircraft}")
        print(f"   Total Flights: {total_flights:,}")
        print(f"   Total Flight Hours: {total_hours:,.1f}")
        
        if active_aircraft > 0:
            print(f"   Avg Flights per Aircraft: {total_flights/active_aircraft:.1f}")
            print(f"   Avg Hours per Aircraft: {total_hours/active_aircraft:.1f}")
        
        print(f"\n🎯 MAIN RESULT: Open 'turkish_airlines_30day_analysis.xlsx' for detailed analysis")
        
    else:
        print("❌ No data retrieved. Please check your API key and try again.")

if __name__ == "__main__":
    main()