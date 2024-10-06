import gradio as gr
import h5py
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import io

def import_file(file_path, keyword):
    with h5py.File(file_path, 'r') as f:
        dataset = f[keyword]
        data = dataset[:]
    return data[0, :, :]

def extract_windows(array, window_size):
    padded_array = np.pad(array, pad_width=1, mode='reflect')
    N, M = array.shape
    windows = np.zeros((N, M, window_size, window_size))
    for i in range(N):
        for j in range(M):
            windows[i, j] = padded_array[i:i + window_size, j:j + window_size]
    return windows

def load_model():
    return joblib.load('/home/saimon/projects/nasaspaceapps/agroia-backend/random_forest_model_new.pkl')

def predict(file):
    data = import_file(file, "precipitation")
    array = data[200:, 200:]
    windows = extract_windows(array, 3)
    features = windows.reshape(-1, 3 * 3)

    model = load_model()
    predictions = model.predict(features)

    reshaped_preds = predictions.reshape(array.shape)

    fig, ax = plt.subplots()
    sns.heatmap(reshaped_preds, xticklabels=[], yticklabels=[])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = buf.getvalue()

    plt.close(fig)

    return img_str

interface = gr.Interface(fn=predict, inputs="file", outputs="image", title="Previsão de Precipitação")
interface.launch()
