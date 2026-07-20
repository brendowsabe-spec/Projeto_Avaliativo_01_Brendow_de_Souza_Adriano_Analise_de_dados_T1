#Conexão e funções utilitárias do MySQL/PostgreSQL (conectar, executar, inserir_em_lote).

from sqlalchemy import create_engine
from urllib.parse import quote_plus

from config import *

def obter_engine():

    senha = quote_plus(DB_PASSWORD)

    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{senha}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return engine