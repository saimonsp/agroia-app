import os
from dotenv import load_dotenv

load_dotenv()  # Carregar variáveis do .env

DATABASE_URL = os.getenv("DATABASE_URL")  # URL do banco de dados
