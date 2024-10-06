import streamlit as st
import h5py
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import os
import tkinter as tk
from tkinter import simpledialog


# Funções que você já tem
def import_file(file_path, keyword):
    with h5py.File(file_path, 'r') as f:
        dataset = f[keyword]
        data = dataset[:]
    return data
def extract_windows(array, window_size):
    padded_array = np.pad(array, pad_width=1, mode='reflect')
    N, M = array.shape
    windows = np.zeros((N, M, window_size, window_size))
    for i in range(N):
        for j in range(M):
            windows[i, j] = padded_array[i:i + window_size, j:j + window_size]
    return windows

def load_model():
    # Obter o caminho absoluto do diretório atual
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, '/home/saimon/projects/nasaspaceapps/agroia-backend/random_forest_model_new.pkl')
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"O arquivo do modelo não foi encontrado: {model_path}")
    
    return joblib.load(model_path)

def predict(file_path,latitudes,longitudes):
    data = import_file(file_path, "precipitation")[0]
    array = data[200:-200, 200:-200]
    windows = extract_windows(array, 3)
    features = windows.reshape(-1, 3 * 3)

    model = load_model()
    predictions = model.predict(features)

    reshaped_preds = predictions.reshape(array.shape)

    fig, ax = plt.subplots()
    sns.heatmap(reshaped_preds, xticklabels=[], yticklabels=[])

    M= array.shape[0]
    N= array.shape[1]
    print(array.shape)
    print(len(latitudes),len(longitudes))
    
    xticks = np.arange(0,M,M//20)
    yticks = np.arange(0,N,N//20)
    print(xticks.shape)
    print(yticks.shape)
    print(reshaped_preds.shape)
    ax.set_yticks(xticks)
    ax.set_xticks(yticks)
    
    ax.set_xticklabels([str(round(x,0))+" °" for x in latitudes[yticks]])
    ax.tick_params(axis='x', rotation=90)

    ax.set_yticklabels([str(round(x,0))+" °" for x in longitudes[xticks]])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return reshaped_preds.tolist(), img_str

# Interface do Streamlit
st.title('Agro.IA - Controle de área produtiva')

uploaded_file = st.file_uploader("Escolha um arquivo .nc4", type=["nc4"])

if uploaded_file is not None:
    # Salvar o arquivo temporariamente
    temp_file_path = 'uploaded_file.nc4'
    with open(temp_file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    
    st.write("Arquivo recebido. Processando...")
    latitudes = import_file(temp_file_path,'lat')
    longitudes = import_file(temp_file_path,"lon")
    latitudes = latitudes[200:-200]
    longitudes = longitudes[200:-200]

    predictions, heatmap_img = predict(temp_file_path,latitudes,longitudes)

    
    st.write("Predições finalizadas!")
    st.image(f"data:image/png;base64,{heatmap_img}")

    # Remover o arquivo temporário após o uso
    os.remove(temp_file_path)
    print(latitudes)
    print(longitudes)

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

# Loop through precipitation files

total_areas = []
for i in range(1):
    
    # Check if latitudes and longitudes are NumPy arrays
    if not isinstance(latitudes, np.ndarray):
        latitudes = np.array(latitudes)
    if not isinstance(longitudes, np.ndarray):
        longitudes = np.array(longitudes)
    
    lat = [latitudes[0],latitudes[-1]]
    lon = [longitudes[0],longitudes[-1]]
      
    total_area = calculate_area(lat,lon)

    total_areas.append(total_area)

# Assuming latitudes and longitudes are already defined
A = latitudes[200:]
B = longitudes[200:]

# Variables to store the selected range limits
lat_start_idx = None
lat_end_idx = None
lon_start_idx = None
lon_end_idx = None

import numpy as np
import pandas as pd

def calculate_productive_area(lat_start_idx, lat_end_idx, lon_start_idx, lon_end_idx, latitudes, longitudes, predictions):
    target_latitudes = np.arange(lat_start_idx, lat_end_idx)
    target_longitudes = np.arange(lon_start_idx, lon_end_idx)

    prod_areas = []
    prod_ratio = []
    total_areas = []

    non_prod_area = 0
    total_area = 0
    predictions = np.array(predictions)
    mask = (predictions < -0).T
    lat1_idx, lat2_idx = target_latitudes[0], target_latitudes[-1]
    lon1_idx, lon2_idx = target_longitudes[0], target_longitudes[-1]
    
    lat1 = latitudes[lat1_idx]
    lat2 = latitudes[lat2_idx]
    lon1 = longitudes[lon1_idx]
    lon2 = longitudes[lon2_idx]
    
    total_area = calculate_area([lat1, lat2], [lon1, lon2])

    # Loop through the grid, skipping masked regions
    for i in target_latitudes:  # Loop over latitude indices
        for j in target_longitudes:  # Loop over longitude indices
            if mask[i, j] and mask[i + 1, j] and mask[i, j + 1] and mask[i + 1, j + 1]:
                # Define the four corners of the small rectangle
                lat = [latitudes[i], latitudes[i + 1]]
                lon = [longitudes[j], longitudes[j + 1]]
                small_area = calculate_area(lat, lon)
                non_prod_area += small_area

    non_prod_area = non_prod_area / (1000 * 1000)
    total_area = total_area / (1000 * 1000)

    total_areas.append(total_area)
    prod_areas.append(total_area - non_prod_area)
    prod_ratio.append((total_area - non_prod_area) / total_area)

    print("Productive area of the region: ", prod_areas)
    print("Productive ratio of the region: ", prod_ratio)

    return prod_areas, prod_ratio, total_areas


def collect_indices(datafile,lat_ref,lon_ref):

  df = pd.read_csv(datafile,header=(0))

  lat_start = df["lat_start"]
  lat_end = df["lat_end"]

  lon_start = df["lon_start"]
  lon_end = df["lon_end"]

  lat_start_idx = lat_start.apply(lambda x: np.argmin(np.abs(latitudes - x)))
  lat_end_idx = lat_end.apply(lambda x: np.argmin(np.abs(latitudes - x)))
  lon_start_idx = lon_start.apply(lambda x: np.argmin(np.abs(latitudes - x)))
  lon_end_idx = lon_end.apply(lambda x: np.argmin(np.abs(latitudes - x)))

  return np.array(lat_start_idx),np.array(lat_end_idx),np.array(lon_start_idx),np.array(lon_end_idx)

lat_start_idxs,lat_end_idxs,lon_start_idxs,lon_end_idxs = collect_indices("/home/saimon/projects/nasaspaceapps/agroia-backend/rectangles.csv",latitudes,longitudes)

for lat_start_idx,lat_end_idx,lon_start_idx,lon_end_idx in zip(lat_start_idxs,lat_end_idxs,lon_start_idxs,lon_end_idxs):
  predictions = np.array(predictions)
  prod_areas, prod_ratio, total_areas = calculate_productive_area(lat_start_idx,lat_end_idx,lon_start_idx,lon_end_idx,latitudes, longitudes, predictions)
  
import csv

# Exemplo de loop e criação de CSV
with open('resultados_areas.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Escreve os cabeçalhos
    writer.writerow(['Lat_Start_Idx', 'Lat_End_Idx', 'Lon_Start_Idx', 'Lon_End_Idx', 'Total_Area', 'Productive_Area', 'Productive_Ratio'])
    
    # Loop para calcular e escrever os resultados para cada conjunto de índices
    for lat_start_idx, lat_end_idx, lon_start_idx, lon_end_idx in zip(lat_start_idxs, lat_end_idxs, lon_start_idxs, lon_end_idxs):
        prod_areas, prod_ratio, total_areas = calculate_productive_area(lat_start_idx, lat_end_idx, lon_start_idx, lon_end_idx, latitudes, longitudes, predictions)
        
        # Escreve os dados no CSV
        for total_area, prod_area, ratio in zip(total_areas, prod_areas, prod_ratio):
            writer.writerow([lat_start_idx, lat_end_idx, lon_start_idx, lon_end_idx, total_area, prod_area, ratio])

print("CSV gerado com sucesso!")
csv1 = pd.read_csv("resultados_areas.csv",header=(0))

csv_data = csv1.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="resultados_areas.csv",
    mime="text/csv"
)
# In[ ]:
