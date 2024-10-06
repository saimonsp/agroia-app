#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from geopy.distance import geodesic


def calculate_area(latitudes,longitudes):
    
    bottom_left = (latitudes[0], longitudes[0])
    bottom_right = (latitudes[0], longitudes[-1])
    top_left = (latitudes[-1], longitudes[0])
    top_right = (latitudes[-1], longitudes[-1])
    
    width = geodesic(bottom_left, bottom_right).meters  # distance along latitude
    height = geodesic(bottom_left, top_left).meters  # distance along longitude
    
    # Calculate the area of the rectangle
    area = width * height/(1000*1000)
    
    return area



# In[ ]:


import numpy as np
import ipywidgets as widgets
from IPython.display import display

# Assuming latitudes and longitudes are already defined
A = latitudes[200:]
B = longitudes[200:]

# Variables to store the selected range limits
lat_start_idx = None
lat_end_idx = None
lon_start_idx = None
lon_end_idx = None

# Function to display and store values at extremities of the selected latitude range
def show_extremities_lat(change):
    global lat_start_idx, lat_end_idx
    range_vals = change['new']
    range_start, range_end = range_vals
    if 0 <= range_start < range_end < len(A):
        lat_start_idx, lat_end_idx = range_start, range_end
        lat_output.value = (f"<b>Latitudes selected:</b> {range_start} to {range_end}<br>"
                            f"<b>A[{range_start}]</b> = {A[range_start]:.2f}, "
                            f"<b>A[{range_end}]</b> = {A[range_end]:.2f}")
    else:
        lat_output.value = "<span style='color:red;'>Please select a valid range within the latitude array.</span>"

# Function to display and store values at extremities of the selected longitude range
def show_extremities_lon(change):
    global lon_start_idx, lon_end_idx
    range_vals = change['new']
    range_start, range_end = range_vals
    if 0 <= range_start < range_end < len(B):
        lon_start_idx, lon_end_idx = range_start, range_end
        lon_output.value = (f"<b>Longitudes selected:</b> {range_start} to {range_end}<br>"
                            f"<b>B[{range_start}]</b> = {B[range_start]:.2f}, "
                            f"<b>B[{range_end}]</b> = {B[range_end]:.2f}")
    else:
        lon_output.value = "<span style='color:red;'>Please select a valid range within the longitude array.</span>"

# Slider widget for latitude range selection
range_slider_lat = widgets.SelectionRangeSlider(
    options=[(f"{i}: {val:.2f}", i) for i, val in enumerate(A)],
    index=(0, len(A) - 1),
    description='Latitudes',
    continuous_update=False,
    layout=widgets.Layout(width='500px'),
    style={'description_width': 'initial'}
)

# Slider widget for longitude range selection
range_slider_lon = widgets.SelectionRangeSlider(
    options=[(f"{i}: {val:.2f}", i) for i, val in enumerate(B)],
    index=(0, len(B) - 1),
    description='Longitudes',
    continuous_update=False,
    layout=widgets.Layout(width='500px'),
    style={'description_width': 'initial'}
)

# Create output widgets to display the selected range
lat_output = widgets.HTML(value="")
lon_output = widgets.HTML(value="")

# Connect the sliders to the display and storage functions
range_slider_lat.observe(show_extremities_lat, names='value')
range_slider_lon.observe(show_extremities_lon, names='value')

# Display the sliders and results using VBox for alignment
display(widgets.VBox([range_slider_lat, lat_output]))
display(widgets.VBox([range_slider_lon, lon_output]))


# In[ ]:


prod_areas = []
prod_ratio = []
total_areas = []

for k,pred in enumerate(pred_col):
    non_prod_area = 0
    total_area = 0
    mask = (pred.reshape(array.shape) < -0).T
    lat1_idx,lat2_idx = target_latitudes[0],target_latitudes[-1]
    lon1_idx,lon2_idx = target_longitudes[0],target_longitudes[-1]
    
    lat1 = latitudes[lat1_idx]
    lat2 = latitudes[lat2_idx]
    lon1 = longitudes[lon1_idx]
    lon2 = longitudes[lon2_idx]
    
    total_area = calculate_area([lat1,lat2],[lon1,lon2])

    # Loop through the grid, skipping masked regions
    count = 0
    for i in target_latitudes:  # Loop over latitude indices
        for j in target_longitudes:  # Loop over longitude indices
            if mask[i, j] and mask[i+1, j] and mask[i, j+1] and mask[i+1, j+1]:
            # Define the four corners of the small rectangle
                lat = [latitudes[i],latitudes[i+1]]
                lon = [longitudes[j],longitudes[j+1]]
                small_area = calculate_area(lat,lon)
                non_prod_area += small_area

    non_prod_area = non_prod_area/(1000*1000)
    total_area = total_area/(1000*1000)
    
    total_areas.append(total_area)
    prod_areas.append(total_area - non_prod_area)
    prod_ratio.append((total_area - non_prod_area)/total_area)

print("Productive area of the region: ", prod_areas)
print("Productive ratio of the region: ", prod_ratio)

