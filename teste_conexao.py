from banco import obter_engine

try:

    engine = obter_engine()

    with engine.connect() as conn:
        print("Conectado com sucesso!")

except Exception as erro:
    print("Erro:", erro)