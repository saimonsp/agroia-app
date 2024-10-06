import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()

# String de conexão com o banco de dados Azure Cosmos DB
DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://agroia-db:vsRdD5wH3tMFj8qSEOZnktv68qtiC3ZTm2M6trU1XNVFcd9Y5572TseXALloAX3jL1vNeuAeOhThACDbfZ3Lsw==@agroia-db.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@agroia-db@")

# Criação do cliente MongoDB
client = MongoClient(DATABASE_URL)

# Acesso ao banco de dados
db = client.get_database("agroia_db")  # Nome do banco de dados que você deseja usar

# Expondo o cliente e o banco de dados para uso em outras partes da aplicação
def get_client():
    return client

async def get_db():
    async with async_session() as session:
        yield session
