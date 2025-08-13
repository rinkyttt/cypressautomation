#!/usr/bin/env python3
"""
Turkish Airlines Fleet Analyzer - Jupyter Notebook Version
Use this in Jupyter notebooks for Turkish Airlines fleet analysis
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
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows


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
        """Retrieve fleet information for Turkish Airlines (ALL aircraft types)"""
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
    
    def get_aircraft_flights(self, registration: str, aircraft_type: str, days_back: int = 30) -> List[FlightData]:
        """Retrieve flight history for a specific aircraft"""
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
    """Main class for analyzing Turkish Airlines entire fleet - Jupyter Notebook compatible"""
    
    def __init__(self, api_key: str):
        self.api = FlightRadar24API(api_key)
        self.all_flights = []
        self.aircraft_stats = {}
        
    def analyze_fleet(self, days_back: int = 30) -> Dict[str, AircraftStats]:
        """Analyze entire Turkish Airlines fleet"""
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
    
    def get_dataframe(self) -> pd.DataFrame:
        """Return aircraft statistics as a pandas DataFrame for Jupyter analysis"""
        if not self.aircraft_stats:
            return pd.DataFrame()
        
        stats_data = []
        for stats in self.aircraft_stats.values():
            stats_data.append({
                'Registration': stats.registration,
                'Aircraft_Type': stats.aircraft_type,
                'Total_Flights': stats.total_flights,
                'Total_Flight_Hours': round(stats.total_flight_time_hours, 1),
                'Total_Flight_Minutes': stats.total_flight_time_minutes,
                'Avg_Flight_Time_Minutes': round(stats.average_flight_time_minutes, 1),
                'First_Flight_Date': stats.first_flight_date,
                'Last_Flight_Date': stats.last_flight_date,
                'Unique_Routes': stats.unique_routes,
                'Most_Common_Route': stats.most_common_route,
                'Top_Route_Count': stats.most_common_route_count
            })
        
        df = pd.DataFrame(stats_data)
        return df.sort_values('Total_Flight_Hours', ascending=False)
    
    def get_flights_dataframe(self) -> pd.DataFrame:
        """Return all flights as a pandas DataFrame for Jupyter analysis"""
        if not self.all_flights:
            return pd.DataFrame()
        
        flights_data = []
        for flight in self.all_flights:
            flights_data.append({
                'Registration': flight.registration,
                'Aircraft_Type': flight.aircraft_type,
                'Flight_Number': flight.flight_number,
                'Departure': flight.departure_airport,
                'Arrival': flight.arrival_airport,
                'Departure_Time': flight.departure_time,
                'Arrival_Time': flight.arrival_time,
                'Duration': flight.flight_duration,
                'Duration_Minutes': flight.duration_minutes,
                'Status': flight.status,
                'Date': flight.date
            })
        
        return pd.DataFrame(flights_data)
    
    def export_to_excel(self, filename: str = "turkish_airlines_fleet_analysis.xlsx"):
        """Export comprehensive data to Excel with multiple worksheets and formatting"""
        if not self.aircraft_stats and not self.all_flights:
            print("No data to export")
            return
        
        # Create workbook
        wb = Workbook()
        
        # Remove default sheet
        wb.remove(wb.active)
        
        # Define styles
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        center_align = Alignment(horizontal="center", vertical="center")
        
        # 1. Aircraft Statistics Sheet
        if self.aircraft_stats:
            ws_stats = wb.create_sheet("Aircraft Statistics")
            df_stats = self.get_dataframe()
            
            # Add headers
            for r in dataframe_to_rows(df_stats, index=False, header=True):
                ws_stats.append(r)
            
            # Format headers
            for cell in ws_stats[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = center_align
                cell.border = border
            
            # Format data cells
            for row in ws_stats.iter_rows(min_row=2):
                for cell in row:
                    cell.border = border
                    if cell.column in [3, 4, 5, 6, 9, 11]:  # Numeric columns
                        cell.alignment = Alignment(horizontal="center")
            
            # Auto-adjust column widths
            for column in ws_stats.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 20)
                ws_stats.column_dimensions[column_letter].width = adjusted_width
        
        # Save the workbook
        wb.save(filename)
        print(f"Excel file exported to {filename}")


# Jupyter Notebook Helper Functions
def analyze_turkish_airlines_fleet(api_key: str, days_back: int = 30) -> TurkishAirlinesFleetAnalyzer:
    """
    Main function for Jupyter notebooks
    
    Usage in Jupyter:
        analyzer = analyze_turkish_airlines_fleet("your_api_key", days_back=30)
        df = analyzer.get_dataframe()
        df.head()
    """
    analyzer = TurkishAirlinesFleetAnalyzer(api_key)
    analyzer.analyze_fleet(days_back)
    return analyzer


def quick_analysis(api_key: str, days_back: int = 30, export_excel: bool = True) -> pd.DataFrame:
    """
    Quick analysis function for Jupyter notebooks
    Returns DataFrame immediately
    
    Usage:
        df = quick_analysis("your_api_key", days_back=30)
        df.head(10)
    """
    analyzer = TurkishAirlinesFleetAnalyzer(api_key)
    analyzer.analyze_fleet(days_back)
    
    if export_excel:
        analyzer.export_to_excel(f"turkish_airlines_{days_back}day_analysis.xlsx")
    
    return analyzer.get_dataframe()