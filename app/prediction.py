import h5py
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64

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
    return joblib.load('random_forest_model_new.pkl')

def predict(file_path):
    # Pipeline de Predição
    data = import_file(file_path, "precipitation")
    array = data[200:, 200:]
    windows = extract_windows(array, 3)
    features = windows.reshape(-1, 3 * 3)

    model = load_model()
    predictions = model.predict(features)

    reshaped_preds = predictions.reshape(array.shape)

    # Para visualização com heatmap
    fig, ax = plt.subplots()
    sns.heatmap(reshaped_preds, xticklabels=[], yticklabels=[])

    # Salvar o heatmap em um objeto de imagem
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')

    # Limpar a imagem
    plt.close(fig)

    return reshaped_preds.tolist(), img_str
