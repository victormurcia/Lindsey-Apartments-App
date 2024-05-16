# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:04:31 2024

@author: vmurc
"""

import pandas as pd
from geopy.geocoders import Nominatim
import time

# Initialize geocoder
geolocator = Nominatim(user_agent="Geopy_Library")

# Function to get coordinates for an address with caching
def get_coordinates(address, geocode_cache):
    if address in geocode_cache:
        return geocode_cache[address]
    
    try:
        location = geolocator.geocode(address, timeout=10)
        if location:
            lat, lon = location.latitude, location.longitude
            geocode_cache[address] = (lat, lon)
            return lat, lon
    except Exception as e:
        print(f"Geocoding error for address {address}: {e}")
    return None, None

# Load data
data = pd.read_csv('apartments.csv')

# Drop duplicates based on the address column
unique_addresses = data.drop_duplicates(subset='Address')

# Initialize geocode cache
geocode_cache = {}

# Add latitude and longitude columns
unique_addresses['Latitude'] = None
unique_addresses['Longitude'] = None

# Geocode addresses
for index, row in unique_addresses.iterrows():
    address = f"{row['Address']}, {row['City']}, {row['State']}"
    lat, lon = get_coordinates(address, geocode_cache)
    if lat is not None and lon is not None:
        unique_addresses.at[index, 'Latitude'] = lat
        unique_addresses.at[index, 'Longitude'] = lon
    time.sleep(1)  # Sleep to avoid hitting API rate limits

# Save results to a new CSV file
unique_addresses.to_csv('geocoded_addresses.csv', index=False)
print("Geocoding complete. Results saved to geocoded_addresses.csv.")
