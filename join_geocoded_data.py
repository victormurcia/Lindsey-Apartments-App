# -*- coding: utf-8 -*-
"""
Created on Thu May 16 16:09:47 2024

@author: vmurc
"""
import pandas as pd

# Load the original apartments data
apartments = pd.read_csv('apartments.csv')

# Load the geocoded addresses data
geocoded_addresses = pd.read_csv('geocoded_addresses.csv')

# Merge the dataframes on the 'Address' column
merged_data = apartments.merge(geocoded_addresses[['Address', 'Latitude', 'Longitude']], on='Address', how='left')

# Save the merged data to a new CSV file
merged_data.to_csv('apartments_with_coordinates.csv', index=False)
print("Data merged and saved to apartments_with_coordinates.csv.")
