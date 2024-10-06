from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

# Cria uma base declarativa para os modelos
Base = declarative_base()

class Prediction(Base):
    __tablename__ = "predictions"  # Nome da tabela no banco de dados

    id = Column(Integer, primary_key=True, index=True)  # ID único para cada previsão
    field = Column(String, index=True)  # Campo que você está prevendo
    predicted_value = Column(Float)  # Valor previsto
    created_at = Column(DateTime)  # Data e hora da previsão

    def __repr__(self):
        return (f"<Prediction(id={self.id}, field={self.field}, "
                f"predicted_value={self.predicted_value}, created_at={self.created_at})>")
