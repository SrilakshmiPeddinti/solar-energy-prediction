#!/usr/bin/env python3
"""
weather_collector.py — Weather Data Collector for Pune using Open-Meteo API.
Gathers: temperature, humidity, cloud cover, solar irradiance, wind speed, rainfall, timestamp.
Calculates energy_output_kwh and outputs a complete datasheet.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
import urllib.request
import urllib.parse

# Set project root to path to allow importing utility files
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Coordinates of Pune, Maharashtra, India
PUNE_LAT = 18.5204
PUNE_LON = 73.8567

def fetch_weather_data(lat: float, lon: float, start_date: str, end_date: str) -> dict:
    """Fetch hourly historical weather data from Open-Meteo API."""
    print(f"Fetching weather data for Lat: {lat}, Lon: {lon} from {start_date} to {end_date}...")
    
    # Base URL for Open-Meteo Archive API (historical data)
    base_url = "https://archive-api.open-meteo.com/v1/archive"
    
    # If the date range is in the future or within the last 2 days, use forecast API
    today = datetime.now().date()
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").date()
    
    # Open-Meteo archive has a delay of 2-5 days. If start date is within last 10 days, use forecast.
    if start_dt > today - timedelta(days=5):
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,cloud_cover,shortwave_radiation,wind_speed_10m,rain",
            "wind_speed_unit": "ms",
            "timezone": "Asia/Kolkata",
            "forecast_days": 14  # Max forecast range
        }
    else:
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": "temperature_2m,relative_humidity_2m,cloud_cover,shortwave_radiation,wind_speed_10m,rain",
            "wind_speed_unit": "ms",
            "timezone": "Asia/Kolkata"
        }
        
    query_string = urllib.parse.urlencode(params)
    url = f"{base_url}?{query_string}"
    
    print(f"API Request URL: {url}")
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            return data
    except Exception as e:
        print(f"Error fetching data from API: {e}", file=sys.stderr)
        sys.exit(1)

def simulate_energy_output(temp: float, irradiance: float, cloud_cover: float) -> float:
    """
    Calculate solar energy output in kWh using the project's physics formula.
    Ref: preprocess.py
    """
    panel_efficiency = 0.18
    panel_area_m2    = 20
    
    # Efficiency decreases as temperature exceeds 25°C
    efficiency_loss  = 1.0 - 0.004 * max(0.0, temp - 25.0)
    
    # Cloud cover factor (dampens output)
    cloud_factor     = 1.0 - 0.8 * (cloud_cover / 100.0)
    
    # Energy output formula
    energy_kwh = (
        irradiance
        * panel_efficiency
        * panel_area_m2
        * efficiency_loss
        * cloud_factor
        / 1000.0
    )
    
    # Clean output
    import random
    # Add a tiny bit of realistic noise, similar to preprocess.py generator
    noise = random.gauss(0, 0.02)
    return max(0.0, round(energy_kwh + noise, 4))

def save_to_csv(weather_data: dict, filepath: str) -> None:
    """Parse JSON response and write to CSV."""
    if "hourly" not in weather_data:
        print("Invalid data format received from weather API.", file=sys.stderr)
        sys.exit(1)
        
    hourly = weather_data["hourly"]
    times = hourly["time"]
    temps = hourly["temperature_2m"]
    humidities = hourly["relative_humidity_2m"]
    clouds = hourly["cloud_cover"]
    irrads = hourly["shortwave_radiation"]
    winds = hourly["wind_speed_10m"]
    rains = hourly["rain"]
    
    # Ensure directories exist
    os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
    
    print(f"Writing dataset to {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        # Header
        f.write("timestamp,temperature_c,humidity_pct,cloud_cover_pct,solar_irradiance_wm2,wind_speed_ms,rainfall_mm,energy_output_kwh\n")
        
        count = 0
        for i in range(len(times)):
            t = times[i]
            # Clean nulls
            temp = temps[i] if temps[i] is not None else 25.0
            hum = humidities[i] if humidities[i] is not None else 50.0
            cloud = clouds[i] if clouds[i] is not None else 0.0
            irr = irrads[i] if irrads[i] is not None else 0.0
            wind = winds[i] if winds[i] is not None else 0.0
            rain = rains[i] if rains[i] is not None else 0.0
            
            # Calculate energy output
            energy = simulate_energy_output(temp, irr, cloud)
            
            f.write(f"{t},{temp},{hum},{cloud},{irr},{wind},{rain},{energy}\n")
            count += 1
            
    print(f"Successfully wrote {count} records to {filepath}.")

def main():
    parser = argparse.ArgumentParser(description="Collect weather data for Pune from Open-Meteo API.")
    parser.add_argument("--start", type=str, default="2023-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, default="2023-12-31", help="End date (YYYY-MM-DD)")
    parser.add_argument("--output", type=str, default="data/raw/pune_weather_data.csv", help="Output CSV path")
    
    args = parser.parse_args()
    
    # 1. Fetch raw weather API data
    api_data = fetch_weather_data(PUNE_LAT, PUNE_LON, args.start, args.end)
    
    # 2. Write CSV with energy simulation
    save_to_csv(api_data, args.output)
    
    print("Gathering of datasheet is complete.")

if __name__ == "__main__":
    main()
