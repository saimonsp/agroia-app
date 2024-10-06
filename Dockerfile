# Usar a imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Definir o comando para rodar a aplicação
CMD ["streamlit", "run", "streamlit run streamlit_app.py, "--server.port=8501", "--server.address=0.0.0.0"]
