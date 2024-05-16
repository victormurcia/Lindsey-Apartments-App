# -*- coding: utf-8 -*-
"""
Created on Thu May 16 13:25:07 2024

@author: vmurc
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import matplotlib.cm as cm
from matplotlib.colors import to_hex
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Function to load and process data
def load_data():
    data = pd.read_csv('apartments_with_coordinates.csv')
    return data

# Function to add a new entry
def add_entry(source, target, value, address, price, num_bedrooms, num_bathrooms, sqft, city, state, latitude, longitude):
    new_entry = pd.DataFrame([[source, target, value, address, price, num_bedrooms, num_bathrooms, sqft, city, state, latitude, longitude]], 
                             columns=['Source', 'Target', 'Value', 'Address', 'Price', 'num_Bedrooms', 'num_Bathrooms', 'SqFt', 'City', 'State', 'Latitude', 'Longitude'])
    with open('apartments_with_coordinates.csv', 'a') as f:
        new_entry.to_csv(f, header=False, index=False)

# Load data
data = load_data()

# Create lists for the nodes and links
nodes = list(set(data['Source']).union(set(data['Target'])))
node_indices = {node: i for i, node in enumerate(nodes)}

# Prepare data for the Sankey diagram
source_indices = data['Source'].map(node_indices)
target_indices = data['Target'].map(node_indices)
values = data['Value']
addresses = data['Address']

# Define the Viridis color palette
viridis = cm.get_cmap('viridis')
node_colors = [to_hex(viridis(i / len(nodes))) for i in range(len(nodes))]
link_colors = [to_hex(viridis(node_indices[source] / len(nodes))) for source in data['Source']]


# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color='black', width=0.5),
        label=nodes,
        color=node_colors
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors,
        hovertemplate='Address: %{customdata}<extra></extra>',
        customdata=addresses
    )
)])

# Set up the layout
fig.update_layout(title_text='Apartment Shopping Process', font_size=10)

# Streamlit setup
st.set_page_config(layout="wide")
st.title('Apartment Shopping Process Dashboard')

# Display Sankey chart across the entire width
st.plotly_chart(fig, use_container_width=True)

# Add new entry form
st.sidebar.title("Add New Entry")
source = st.sidebar.selectbox("Source", options=nodes)
target = st.sidebar.selectbox("Target", options=nodes)
value = st.sidebar.number_input("Value", min_value=1)
address = st.sidebar.text_input("Address")
price = st.sidebar.number_input("Price", min_value=0)
num_bedrooms = st.sidebar.number_input("Number of Bedrooms", min_value=0)
num_bathrooms = st.sidebar.number_input("Number of Bathrooms", min_value=0)
sqft = st.sidebar.number_input("Square Feet", min_value=0)
city = st.sidebar.text_input("City")
state = st.sidebar.text_input("State")
latitude = st.sidebar.number_input("Latitude", min_value=-90.0, max_value=90.0)
longitude = st.sidebar.number_input("Longitude", min_value=-180.0, max_value=180.0)

if st.sidebar.button("Add Entry"):
    add_entry(source, target, value, address, price, num_bedrooms, num_bathrooms, sqft, city, state, latitude, longitude)
    st.sidebar.success("New entry added! Please refresh the page to see the updated chart.")


# Generate histograms with different colors
def plot_histogram(data, column, color, nbins=10):
    fig = px.histogram(data, x=column, nbins=nbins, color_discrete_sequence=[color])
    fig.update_layout(clickmode='event+select')
    return fig

st.title('Additional Data Analysis')

# Arrange histograms in a single row over 4 columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.header('Price')
    fig_price = plot_histogram(data, 'Price', 'Violet')
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.header('Bedrooms')
    fig_bedrooms = plot_histogram(data, 'num_Bedrooms', 'Indigo')
    st.plotly_chart(fig_bedrooms, use_container_width=True)

with col3:
    st.header('Bathrooms')
    fig_bathrooms = plot_histogram(data, 'num_Bathrooms', 'Lavender')
    st.plotly_chart(fig_bathrooms, use_container_width=True)

with col4:
    st.header('Square Feet')
    fig_sqft = plot_histogram(data, 'SqFt', 'Thistle')
    st.plotly_chart(fig_sqft, use_container_width=True)

# Manual filters
st.title('Filter Apartments')

# Arrange filters in a single row
filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)

with filter_col1:
    price_range = st.slider('Price Range', min_value=int(data['Price'].min()), max_value=int(data['Price'].max()), value=(int(data['Price'].min()), int(data['Price'].max())))

with filter_col2:
    bedroom_range = st.slider('Number of Bedrooms', min_value=int(data['num_Bedrooms'].min()), max_value=int(data['num_Bedrooms'].max()), value=(int(data['num_Bedrooms'].min()), int(data['num_Bedrooms'].max())))

with filter_col3:
    bathroom_range = st.slider('Number of Bathrooms', min_value=int(data['num_Bathrooms'].min()), max_value=int(data['num_Bathrooms'].max()), value=(int(data['num_Bathrooms'].min()), int(data['num_Bathrooms'].max())))

with filter_col4:
    sqft_range = st.slider('Square Feet', min_value=int(data['SqFt'].min()), max_value=int(data['SqFt'].max()), value=(int(data['SqFt'].min()), int(data['SqFt'].max())))

with filter_col5:
    selected_cities = st.multiselect('Select Cities', options=data['City'].unique(), default=data['City'].unique())

# Filter data based on the selected ranges and cities
filtered_data = data[
    (data['Price'] >= price_range[0]) & (data['Price'] <= price_range[1]) &
    (data['num_Bedrooms'] >= bedroom_range[0]) & (data['num_Bedrooms'] <= bedroom_range[1]) &
    (data['num_Bathrooms'] >= bathroom_range[0]) & (data['num_Bathrooms'] <= bathroom_range[1]) &
    (data['SqFt'] >= sqft_range[0]) & (data['SqFt'] <= sqft_range[1]) &
    (data['City'].isin(selected_cities))
]

# Remove duplicate addresses and drop the 'Value' column
filtered_data = filtered_data.drop_duplicates(subset='Address').drop(columns=['Value','Source','Target']).reset_index(drop=True)

# Display the filtered dataframe
st.subheader('Filtered Apartments')
st.dataframe(filtered_data)

# Display map
st.subheader('Map of Filtered Apartments')
map_center = [35.787743, -78.644257]  # Center the map around North Carolina
m = folium.Map(location=map_center, zoom_start=8)
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for index, row in filtered_data.iterrows():
    lat, lon = row['Latitude'], row['Longitude']
    if pd.notnull(lat) and pd.notnull(lon):
        folium.Marker(
            location=[lat, lon],
            popup=f"{row['Address']}\nPrice: ${row['Price']}\nBedrooms: {row['num_Bedrooms']}\nBathrooms: {row['num_Bathrooms']}\nSqFt: {row['SqFt']}"
        ).add_to(marker_cluster)

st_folium(m, width=700)