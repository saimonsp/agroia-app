# Usar a imagem base do Python
FROM python:3.9-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos de requisitos e instalar as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação
COPY . .

# Copiar o arquivo de dados para o diretório da aplicação
COPY 3B-DAY.MS.MRG.3IMERG.20211116-S000000-E235959.V07B.nc4 /app/

# Definir o comando para rodar a aplicação
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8502", "--server.address=0.0.0.0"]
